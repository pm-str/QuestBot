import logging

from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.web.api.serializers import UpdateModelSerializer
from apps.web.models import AppUser, Bot, CallbackQuery, Chat, Message, Update

logger = logging.getLogger(__name__)


class ProcessWebHookAPIView(CreateModelMixin, GenericViewSet):
    serializer_class = UpdateModelSerializer
    queryset = Update.objects.all()

    def create(self, request, *args, **kwargs):
        self.request.data['hook_id'] = kwargs.get('hook_id', None)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(request.data)
        return Response(
            request.data,
            headers=headers,
            status=status.HTTP_201_CREATED,
        )

    @staticmethod
    def handle_message(data):
        bot = data['bot']
        user, _ = AppUser.objects.get_or_create(**data['message']['from_user'])
        chat, _ = Chat.objects.get_or_create(**data['message']['chat'])
        message, _ = Message.objects.get_or_create(
            from_user=user,
            chat=chat,
            date=data['message']['date'],
            text=data['message']['text'],
            message_id=data['message']['message_id'],
        )
        update, _ = Update.objects.get_or_create(
            bot=bot,
            message=message,
            update_id=data['update_id'],
        )
        return update

    @staticmethod
    def message_from_callback(callback):
        if 'message' in callback:
            user, _ = AppUser.objects.get_or_create(
                **callback['message']['from']
            )
            chat, _ = Chat.objects.get_or_create(
                **callback['message']['chat']
            )

            message, _ = Message.objects.get_or_create(
                message_id=callback['message']['message_id'],
                from_user=user,
                chat=chat,
                date=callback['message']['date'],
                text=callback['message']['text']
            )
        else:
            message = None
        return message

    def handle_callback(self, data):
        bot = data['bot']
        user, _ = AppUser.objects.get_or_create(
            **data['callback_query']['from_user']
        )
        chat, _ = Chat.objects.get_or_create(**data['callback_query']['chat'])
        callback_query, _ = CallbackQuery.objects.get_or_create(
            from_user=user,
            message=message,
            data=data['callback_query']['data'],
            callback_id=data['callback_query']['id'],
        )
        message = self.message_from_callback(data['callback_query'])
        update, _ = Update.objects.get_or_create(
            bot=bot,
            message=message,
            update_id=data['update_id'],
        )
        return update

    def perform_create(self, serializer):
        data = serializer.validated_data

        if 'message' in data:
            update = self.handle_message(data)
        else:
            update = self.handle_callback(data)

        return update

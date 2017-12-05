from datetime import datetime
from constance import config
from django.conf import settings

import time

from rest_framework import serializers

from apps.web.models import Update, Message, AppUser, Chat, CallbackQuery, Bot


class TelegramBot(object):
    def set_context(self, serializer_field):
        bot_id = serializer_field.context['request'].data['hook_id']

        self.bot = Bot.objects.get(id=bot_id)

    def __call__(self):
        return self.bot


class ChatModelSerializer(serializers.ModelSerializer):
    id = serializers.CharField(validators=[])

    class Meta:
        model = Chat


class AppUserModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        default=getattr(config, settings.TELEGRAM_DEFAULT_PASS),
        read_only=True,
    )
    username = serializers.CharField(validators=[])

    class Meta:
        model = AppUser


class TimeStampField(serializers.Field):
    def to_representation(self, value: datetime):
        return time.mktime(value.timetuple())

    def to_internal_value(self, data: int):
        return datetime.fromtimestamp(data)


class MessageModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['from'] = self.fields['from_user']
        del self.fields['from_user']

    message_id = serializers.CharField()
    from_user = AppUserModelSerializer()
    forward_from = AppUserModelSerializer(
        allow_null=True,
        required=False,
        validators=[]
    )
    date = TimeStampField()
    chat = ChatModelSerializer()

    class Meta:
        model = Message
        fields = (
            'message_id',
            'date',
            'chat',
            'from_user',
            'forward_from',
            'text',
        )


class CallbackQueryModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['from'] = self.fields['from_user']
        del self.fields['from_user']

    message = MessageModelSerializer()
    from_user = AppUserModelSerializer()

    class Meta:
        model = CallbackQuery
        field = (
            'id',
            'message',
            'data',
            'from_user',
        )


class UpdateModelSerializer(serializers.ModelSerializer):
    bot = serializers.HiddenField(default=TelegramBot())
    message = MessageModelSerializer(
        required=False,
        allow_null=True
    )
    callback_query = CallbackQueryModelSerializer(
        required=False,
        allow_null=True
    )

    class Meta:
        model = Update
        fields = (
            'update_id',
            'bot',
            'message',
            'callback_query',
        )

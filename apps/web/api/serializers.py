import time
from django.utils import timezone

from django.conf import settings

from rest_framework import serializers

from constance import config

from apps.web.models import AppUser, Bot, CallbackQuery, Chat, Message, Update
from apps.web.models.message import PhotoSize


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
        fields = '__all__'


class AppUserModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        default=getattr(config, settings.TELEGRAM_DEFAULT_PASS),
        read_only=True,
    )
    username = serializers.CharField(validators=[])

    class Meta:
        model = AppUser
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
            'is_bot',
            'language_code',
            'password',
        ]


class TimeStampField(serializers.Field):
    def to_representation(self, value: timezone):
        return time.mktime(value.timetuple())

    def to_internal_value(self, data: int):
        return timezone.datetime.fromtimestamp(data)


class PhotoSizeSerializer(serializers.ModelSerializer):
    message = serializers.HiddenField(default=None, read_only=False)

    class Meta:
        model = PhotoSize
        fields = '__all__'


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
    photo = PhotoSizeSerializer(
        many=True,
        required=False,
    )

    class Meta:
        model = Message
        fields = (
            'message_id',
            'date',
            'chat',
            'photo',
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
        fields = (
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

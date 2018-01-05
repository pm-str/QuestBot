import logging
import textwrap
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from constance import config
from telegram.bot import Bot as TelegramBot
from telegram.error import InvalidToken, TelegramError

from apps.web.validators import token_validator

from .abstract import TimeStampModel

logger = logging.getLogger(__name__)


class BotDescriptor(object):
    def __get__(self, instance, owner):
        if not instance._bot:
            instance.init_bot()
        return instance._bot

    def __set__(self, instance, value):
        instance._bot = value


class Bot(TimeStampModel):
    _bot = None
    bot: TelegramBot = BotDescriptor()
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    token = models.CharField(
        max_length=1000,
        unique=True,
        verbose_name='Bot token',
        validators=[token_validator],
    )
    name = models.CharField(max_length=250, verbose_name='Bot name')
    user_api = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        related_name='telegram_bot',
        verbose_name='Owner',
        help_text=_('API user. Automatically retrieved from Telegram'),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    enabled = models.BooleanField(
        default=True,
        verbose_name='Bot enabled',
        help_text=_('Define if bot is enabled. Active by default')
    )
    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name='telegram_bots',
        verbose_name='Owner',
        help_text=_('User that owns this bot'),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('Bot')
        verbose_name_plural = _('Bots')

    def __str__(self):
        return self.name

    def clean(self):
        """Perform custom validation

        Check if token is valid.

        Throw validation error, in otherwise

        """
        try:
            self.init_bot()
        except InvalidToken:
            raise ValidationError(
                {'token': _('Your token is not valid.')})

    def init_bot(self):
        """Initialize bot instance through Telegram API"""

        self._bot = TelegramBot(token=self.token)

    def get_file(self, file_id):
        """Download file by link"""
        return self.bot.getFile(file_id)

    def set_webhook(self, url):
        """Set webhook for Telegram bot"""
        self._bot.set_webhook(url=url)

    @property
    def is_initialized(self) -> bool:
        """Return if bot is initialized or only instance created"""
        return self._bot is not None

    @property
    def hook_id(self) -> str:
        """Return hook_id, i.e. bot id"""
        return str(self.id)

    def delete_message(self, chat_id, message_id):
        """Delete message method

        Commonly is used to remove message from previous callback queries,
        for instance, it can be inline keyboard's markup

        """
        try:
            self.bot.delete_message(chat_id=chat_id, message_id=message_id)
        except TelegramError as r:
            logger.error("""Error on message deleting has been occurred. chat:
            {}, message: {}""".format(chat_id, message_id))

    def edit_message_reply_markup(self, chat_id, message_id):
        self.bot.editMessageReplyMarkup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup='',
        )

    def send_message(
            self,
            chat_id,
            text,
            keyboard=None,
            reply_message_id=None,
            disable_notifications=False,
            disable_links_preview=False,
    ):
        parse_mode = getattr(config, settings.TELEGRAM_PARSE_MODE)

        msg_texts = []

        # Text of the message to be sent. Max 4096 characters.
        # Also found as telegram.constants.MAX_MESSAGE_LENGTH
        for text in text.strip().split('__'):
            for part in textwrap.wrap(text, 4096, replace_whitespace=False):
                msg_texts.append(part)

        for msg in msg_texts:
            try:
                self.bot.send_message(
                    chat_id=chat_id,
                    text=msg,
                    parse_mode=parse_mode,
                    disable_web_page_preview=disable_links_preview,
                    disable_notification=disable_notifications,
                    reply_message_id=reply_message_id,
                    reply_markup=keyboard,
                    timeout=5000,
                )
            except TelegramError as error:
                logger.error("""Error on message send has been occurred. chat:
                {}, text: {}, reply_message: {}, markup: {}, error: {}
                """.format(chat_id, msg, reply_message_id, keyboard, error))

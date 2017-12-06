import re
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from telegram.bot import Bot as TelegramBot
from telegram.error import InvalidToken

from apps.config import settings

from .abstract import TimeStampModel


def validate_token(value):
    if not re.match('[0-9]+:[-_a-zA-Z0-9]+', value):
        raise ValidationError(
            _("%(value)s is not a valid token"),
            params={'value': value}
        )


class Bot(TimeStampModel):
    _bot = None
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    token = models.CharField(
        max_length=1000,
        unique=True,
        verbose_name='Bot token',
        validators=[validate_token],
    )
    name = models.CharField(max_length=250, verbose_name='Bot name')
    user_api = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        related_name='telegram_bot',
        verbose_name='Owner',
        help_text=_('API user. Automatically retrieved from Telegram'),
        blank=True,
        null=True,
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
        return self._bot.getFile(file_id)

    def set_webhook(self, url):
        """Set webhook for Telegram bot"""
        self._bot.set_webhook(webhook_url=url)

    @property
    def is_initialized(self) -> bool:
        """Return if bot is initialized or only instance created"""
        return self._bot is not None

    @property
    def hook_id(self) -> str:
        """Return hook_id, i.e. bot id"""
        return str(self.id)

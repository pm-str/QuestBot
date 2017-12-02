from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.config import settings

from .abstract import TimeStampModel


class Message(TimeStampModel):
    message_id = models.BigIntegerField(
        verbose_name='Message id',
        db_index=True,
        help_text='Telegram message id retrieved from API'
    )
    date = models.DateTimeField(
        verbose_name=_('Date'),
        help_text='Date the message was sent',
    )
    forward_from = models.ForeignKey(
        to='AppUser',
        null=True,
        blank=True,
        related_name='forwarded_messages',
        verbose_name=_('Sender of the original message')
    )
    from_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name='messages',
        verbose_name='From User',
        help_text=_('Retrieved user from'),
    )
    chat = models.ForeignKey(
        to='Chat',
        related_name='messages',
        verbose_name='Chat id',
        help_text='Retrieved from Telegram API chat id',
    )
    text = models.CharField(max_length=2500, verbose_name='Message text')

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    def __str__(self):
        return self.message_id

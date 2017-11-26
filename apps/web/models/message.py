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
    from_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name='messages',
        verbose_name='From User',
        help_text=_('Retrieved user from'),
    )
    handler = models.ForeignKey(
        to='Handler',
        related_name='messages',
        verbose_name='Handler',
        help_text=_('Handler contains expression needed to process a message'),
        blank=True,
        null=True,
    )
    chat = models.BigIntegerField(
        verbose_name='Chat id',
        help_text='Retrieved from Telegram API chat id'
    )
    text = models.CharField(max_length=2500, verbose_name='Message text')

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    def __str__(self):
        return self.message_id

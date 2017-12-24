from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.config import settings

from .abstract import TimeStampModel


class PhotoSize(TimeStampModel):
    file_id = models.CharField(
        max_length=1000,
        primary_key=True,
        unique=True,
        db_index=True,
        help_text=_('Unique identifier for this file.'),
        verbose_name=_('File ID'),
    )
    width = models.IntegerField(verbose_name=_('Image width'))
    height = models.IntegerField(verbose_name=_('Image height'))
    file_size = models.IntegerField(verbose_name=_('File size'))
    message = models.ForeignKey(
        to='Message',
        related_name='photos',
        verbose_name=_('From message'),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )


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
        verbose_name=_('Sender of the original message'),
        on_delete=models.CASCADE,
    )
    from_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name='messages',
        verbose_name='From User',
        help_text=_('Retrieved user from'),
        on_delete=models.CASCADE,
    )
    chat = models.ForeignKey(
        to='Chat',
        related_name='messages',
        verbose_name='Chat id',
        help_text='Retrieved from Telegram API chat id',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        max_length=2500,
        verbose_name='Message text',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    def __str__(self):
        return str(self.message_id)

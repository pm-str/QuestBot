from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from telegram import TelegramError

from .abstract import TimeStampModel


NOT_STARTED = 'not_started'
PENDING = 'pending'
SUCCEEDED = 'succeeded'
FAILED = 'failed'

STATUS_CHOICES = (
    (NOT_STARTED, _('Not started')),
    (PENDING, _('Pending')),
    (SUCCEEDED, _('Succeeded')),
    (FAILED, _('Failed')),
)


class Event(TimeStampModel):
    name = models.CharField(verbose_name='Event name', max_length=255)
    bot = models.ForeignKey('Bot', null=True)
    chat = models.ForeignKey('Chat', null=True)
    send_date = models.DateTimeField(
        verbose_name='Time to send on',
        default=timezone.now(),
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=NOT_STARTED,
    )
    message = models.ForeignKey(
        to='Message',
        verbose_name='Reply to message',
        null=True,
        blank=True,
    )
    response = models.ForeignKey(
        to='Response',
        verbose_name='Responses with data',
        null=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.status == NOT_STARTED:
            try:
                self.status = PENDING
                self.response.send_message(
                    bot=self.bot,
                    chat=self.chat,
                    message=self.message,
                )
            except TelegramError:
                self.status = FAILED
            else:
                self.status = SUCCEEDED

        super().save(*args, **kwargs)

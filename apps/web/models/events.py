from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from telegram import TelegramError

from apps.web.models.user import AppUser

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
    name = models.CharField(
        verbose_name='Event name',
        max_length=255,
    )
    bot = models.ForeignKey(
        to='Bot',
        null=True,
        on_delete=models.CASCADE,
    )
    chat = models.ForeignKey(
        to='Chat',
        null=True,
        on_delete=models.CASCADE,
    )
    send_date = models.DateTimeField(
        verbose_name='Time to send on',
        default=timezone.now,
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
        on_delete=models.CASCADE,
    )
    response = models.ForeignKey(
        to='Response',
        verbose_name='Responses with data',
        null=True,
        on_delete=models.CASCADE,
    )
    move_user_to = models.ForeignKey(
        to='Step',
        verbose_name=_('Mover user to step'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.move_user_to:
            AppUser.objects.filter(username=self.chat.username).update(
                step=self.move_user_to,
            )

        if self.status == NOT_STARTED:
            try:
                self.status = PENDING
                self.response.send_response(
                    bot=self.bot,
                    chat=self.chat,
                    message=self.message,
                    eta=self.send_date,
                )
            except TelegramError:
                self.status = FAILED
            else:
                self.status = SUCCEEDED

        super().save(*args, **kwargs)

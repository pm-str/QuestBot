from django.db import models

from .abstract import TimeStampModel


class Event(TimeStampModel):
    name = models.CharField(verbose_name='Event name', max_length=255)
    send_date = models.DateTimeField(verbose_name='Time to send on')
    responses = models.ManyToManyField(
        to='Response',
        related_name='events',
        verbose_name='Responses that are used in the event',
        blank=True,
    )
    users = models.ManyToManyField(
        verbose_name='Users to send to',
        to='AppUser',
        related_name='events',
        blank=True,
    )

    def __str__(self):
        return self.name

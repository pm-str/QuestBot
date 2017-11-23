from django.db import models

from .abstract import TimeStampModel


class Response(TimeStampModel):
    title = models.CharField(
        verbose_name='Response title',
        max_length=1000,
    )
    message = models.CharField(
        verbose_name='Response message',
        max_length=1000,
        null=True,
        blank=True,
    )
    file = models.FileField(
        verbose_name='Attached file',
        null=True,
        blank=True,
    )
    redirect_to = models.ForeignKey(
        to='AppUser',
        related_name='redirected_responses',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title

from django.db import models

from .abstract import TimeStampModel


class Response(TimeStampModel):
    title = models.CharField(verbose_name='Response title', max_length=1000)
    on_true = models.BooleanField(
        verbose_name='Triggering on true',
        default=True,
    )
    message = models.ForeignKey(
        to='Message',
        verbose_name='Response message',
        related_name='responses',
        null=True,
        blank=True,
    )
    handler = models.ForeignKey(
        verbose_name='Attached handler to',
        to='Handler',
        related_name='responses',
    )
    redirect_to = models.ManyToManyField(
        verbose_name='Redirect to users',
        to='AppUser',
        related_name='redirected_responses',
        blank=True,
    )

    def __str__(self):
        return self.title

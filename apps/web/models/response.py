from django.db import models

from .abstract import TimeStampModel


class Response(TimeStampModel):
    title = models.CharField(verbose_name='Response title', max_length=1000)
    on_true = models.BooleanField(
        verbose_name='Triggering on true',
        default=True,
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
    requests = models.ForeignKey(
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

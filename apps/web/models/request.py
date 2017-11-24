from django.db import models
from .abstract import TimeStampModel


class Request(TimeStampModel):
    steps = models.ForeignKey(to='Step', related_name='requests')
    ids_expression = models.CharField(
        max_length=500,
        verbose_name="Mathematics expression from ids. Allowed '+*()!'",
        default='{}'
    )
    allowed = models.ManyToManyField(
        to='AppUser',
        related_name='requests',
        blank=True,
    )
    slug = models.CharField(
        verbose_name="Request command",
        max_length=255,
    )
    title = models.CharField(
        verbose_name="Request title",
        max_length=255,
    )

    def __str__(self):
        return self.title


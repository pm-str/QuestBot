from django.db import models
from django.utils.translation import ugettext_lazy as _

from .abstract import TimeStampModel


class Handler(TimeStampModel):
    steps = models.ForeignKey(to='Step', related_name='handlers')
    ids_expression = models.CharField(
        max_length=500,
        verbose_name='Mathematics expression',
        help_text=_("Allowed / +*()! /. A set of rules by condition's id"),
        default='{}'
    )
    allowed = models.ManyToManyField(
        to='AppUser',
        related_name='handlers',
        blank=True,
    )
    slug = models.CharField(
        verbose_name="Handler command",
        max_length=255,
        blank=True,
        null=True,
    )
    step_on_success = models.SmallIntegerField(
        verbose_name='Step on success',
        help_text='Move to this step if mathematics expression truthful',
        null=True,
        blank=True,
    )
    step_on_error = models.SmallIntegerField(
        verbose_name='Step on error',
        help_text='Move to this step if mathematics expression wrongful',
        null=True,
        blank=True,
    )
    title = models.CharField(verbose_name="Handler title", max_length=255)

    class Meta:
        verbose_name = _('Handler')
        verbose_name_plural = _('Handlers')

    def __str__(self):
        return self.title

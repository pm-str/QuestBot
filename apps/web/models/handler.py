from django.db import models
from django.utils.translation import ugettext_lazy as _

from .abstract import TimeStampModel


class Handler(TimeStampModel):
    steps = models.ForeignKey(to='Step', related_name='handlers')
    ids_expression = models.CharField(
        max_length=500,
        verbose_name="Mathematics expression from ids. Allowed '+*()!'",
        help_text=_('Validate a set of rules by condition id'),
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
    title = models.CharField(verbose_name="Handler title", max_length=255)

    class Meta:
        verbose_name = _('Handler')
        verbose_name_plural = _('Handlers')

    def __str__(self):
        return self.title

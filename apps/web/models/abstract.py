from django.db import models
from django.utils.translation import ugettext_lazy as _


class TimeStampModel(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
        help_text=_('Entity created at'),
        null=True,
    )
    modified = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at'),
        help_text=_('Entity created at'),
        null=True,
    )

    class Meta:
        abstract = True

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.web.querysets import StepQuerySet
from apps.web.validators import only_initial
from .abstract import TimeStampModel


class Step(TimeStampModel):
    objects = StepQuerySet.as_manager()
    is_initial = models.BooleanField(default=False, validators=[only_initial])
    title = models.CharField(verbose_name=_('Step title'), max_length=255)
    number = models.PositiveIntegerField(verbose_name=_('Step Number'))
    quest = models.ForeignKey(to='Quest', related_name='steps')

    def __str__(self):
        return f'{self.title} - {self.number}'

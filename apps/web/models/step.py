from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.web.querysets import StepQuerySet
from .abstract import TimeStampModel


def only_initial(value):
    if value and Step.objects.filter(is_initial=True).count():
        raise ValidationError(
            'Only one field must be unique',
            code='invalid',
        )


class Step(TimeStampModel):
    objects = StepQuerySet.as_manager()
    is_initial = models.BooleanField(default=False, validators=[only_initial])
    title = models.CharField(verbose_name=_('Step title'), max_length=255)
    number = models.PositiveIntegerField(verbose_name=_('Step Number'))
    quest = models.ForeignKey(to='Quest', related_name='steps')

    def __str__(self):
        return f'{self.title} - {self.number}'

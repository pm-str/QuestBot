from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.web.querysets import StepQuerySet
from apps.web.validators import initial_step_validator

from .abstract import TimeStampModel


class Step(TimeStampModel):
    objects = StepQuerySet.as_manager()
    is_initial = models.BooleanField(default=False, validators=[initial_step_validator])
    title = models.CharField(verbose_name=_('Step title'), max_length=255)
    number = models.SmallIntegerField(verbose_name=_('Step Number'))
    quest = models.ForeignKey(
        to='Quest',
        related_name='steps',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('number', 'title',)

    def __str__(self):
        return f'{self.title} - {self.number}'

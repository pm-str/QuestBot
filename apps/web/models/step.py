from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.web.querysets import StepQuerySet

from .abstract import TimeStampModel


class Step(TimeStampModel):
    objects = StepQuerySet.as_manager()
    is_initial = models.BooleanField()
    title = models.CharField(verbose_name=_('Step title'), max_length=255)
    number = models.SmallIntegerField(verbose_name=_('Step Number'))
    quest = models.ForeignKey(
        to='Quest',
        related_name='steps',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('number', 'title',)

    def full_clean(self, *args, **kwargs):
        super().full_clean(*args, **kwargs)

        steps = self.quest.steps.all()

        temp = steps.filter(is_initial=True).first()
        if self.is_initial and temp and temp.id != self.id:
            raise ValidationError({
                'is_initial': 'Only one step must be initial',
            })

        temp = steps.filter(number=self.number).first()
        if temp and temp.id != self.id:
            raise ValidationError({
                'number': "This number exists",
            })

    def __str__(self):
        return f'{self.title} - {self.number}'

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

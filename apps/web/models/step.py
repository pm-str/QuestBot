from django.db import models
from django.utils.translation import ugettext_lazy as _

from .abstract import TimeStampModel

NOT_STARTED = 'not_started'
IN_PROCESS = 'in_process'
FINISHED = 'finished'

choices = (
    (NOT_STARTED, _("Not started")),
    (IN_PROCESS, _("In process")),
    (FINISHED, _("Finished"))
)


class Step(TimeStampModel):
    title = models.CharField(verbose_name='Step title', max_length=255)
    number = models.PositiveIntegerField(verbose_name="Step Number")
    quest = models.ForeignKey(to='Quest', related_name='steps')
    status = models.CharField(
        verbose_name="Status of step",
        choices=choices,
        default=NOT_STARTED,
        max_length=255,
    )

    def __str__(self):
        return f'{self.title} - {self.number}'

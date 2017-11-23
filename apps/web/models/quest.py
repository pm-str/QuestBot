from django.db import models

from .abstract import TimeStampModel


class Quest(TimeStampModel):
    title = models.CharField(verbose_name="Quest name", max_length=255)
    description = models.TextField(
        verbose_name="Quest description",
        max_length=1000,
    )

    def __str__(self):
        return self.title

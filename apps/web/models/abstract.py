from django.db import models


class TimeStampModel(models.Model):
    created = models.DateField(auto_now_add=True, verbose_name="Created at")
    modified = models.DateField(auto_now=True, verbose_name="Updated at")

    class Meta:
        abstract = True

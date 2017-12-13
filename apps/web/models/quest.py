from django.db import models
from django.utils.translation import ugettext_lazy as _

from .abstract import TimeStampModel


class Quest(TimeStampModel):
    title = models.CharField(verbose_name="Quest name", max_length=255)
    description = models.TextField(
        verbose_name="Quest description",
        max_length=1000,
    )
    bot = models.OneToOneField(
        to='Bot',
        related_name='quest',
        verbose_name=_('Connected bot'),
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title

    def initialize_user(self, user):
        """If user has no any assigned steps, there should be added initial one

        Add one unique step with active ``is_initial`` flag

        """
        user.step = self.steps.initial()
        user.save()

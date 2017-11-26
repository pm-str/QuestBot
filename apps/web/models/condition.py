from django.db import models
from django.utils.translation import ugettext_lazy as _

from .abstract import TimeStampModel

FULL_COINCIDENCE = 'full_coincidence'
TO_BE_IN = 'to_be_in'
STARTS_WITH = 'starts_with'
ENDS_WITH = 'ends_with'
CONTAIN_AN_IMAGE = 'contain_an_image'
CONTAIN_A_FILE = 'contain_a_file'
CONTAIN_AN_AUDIO = 'contain_an_audio'
CONTAIN_A_VIDEO = 'contain_a_video'
RECEIVED_BEFORE = 'received_before'
RECEIVED_AFTER = 'received_after'

CHOICES = (
    (FULL_COINCIDENCE, _('Full coincidence')),
    (TO_BE_IN, _('To be in')),
    (STARTS_WITH, _('Starts with')),
    (ENDS_WITH, _('Ends with')),
    (CONTAIN_AN_IMAGE, _('Contain an image')),
    (CONTAIN_A_FILE, _('Contain a file')),
    (CONTAIN_AN_AUDIO, _('Contain a audio')),
    (CONTAIN_A_VIDEO, _('Contain a video')),
    (RECEIVED_BEFORE, _('Received before')),
    (RECEIVED_AFTER, _('Received after')),
)


class Condition(TimeStampModel):
    value = models.CharField(verbose_name='Proper answer', max_length=1000)
    rule = models.CharField(
        verbose_name='Step title',
        max_length=255,
        choices=CHOICES,
        default=FULL_COINCIDENCE,
    )
    handler = models.ForeignKey(
        to='Handler',
        verbose_name='Attached to handler',
        related_name='conditions',
    )
    pattern = models.CharField(
        max_length=500,
        verbose_name='Regex pattern',
        help_text='Helps to determine the truth for some rules'
    )

    def __str__(self):
        return f'{self.rule}'

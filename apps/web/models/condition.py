import re

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.web.models.update import Update
from .abstract import TimeStampModel

FULL_COINCIDENCE = 'full_coincidence'
TO_BE_IN = 'to_be_in'
STARTS_WITH = 'starts_with'
ENDS_WITH = 'ends_with'
MATCH_REGEX = 'match_regex'
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
    (MATCH_REGEX, _('Match regex')),
    (CONTAIN_AN_IMAGE, _('Contain an image')),
    (CONTAIN_A_FILE, _('Contain a file')),
    (CONTAIN_AN_AUDIO, _('Contain a audio')),
    (CONTAIN_A_VIDEO, _('Contain a video')),
    (RECEIVED_BEFORE, _('Received before')),
    (RECEIVED_AFTER, _('Received after')),
)


class Condition(TimeStampModel):
    value = models.CharField(verbose_name='Answer or pattern', max_length=1000)
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

    def __str__(self):
        return f'{self.rule}'

    def is_match_to_rule(self, update: Update):
        """Check if update object match to the specified rule"""
        msg = update.get_message()
        msg_text = msg.text.strip()

        if self.rule == FULL_COINCIDENCE:
            return msg_text == self.value
        elif self.rule == TO_BE_IN:
            return msg_text in self.value
        elif self.rule == STARTS_WITH:
            return msg_text.startswith(self.value)
        elif self.rule == ENDS_WITH:
            return msg_text.endswith(self.value)
        elif self.rule == MATCH_REGEX:
            return re.match(self.value, msg_text)
        elif self.rule == CONTAIN_AN_IMAGE:
            return msg.images.count()

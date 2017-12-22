from django.db import models
from django.utils.translation import ugettext_lazy as _

from .abstract import TimeStampModel


class Chat(TimeStampModel):
    PRIVATE = 'private'
    GROUP = 'group'
    SUPERGROUP = 'supergroup'
    CHANNEL = 'channel'

    CHOICES = (
        (PRIVATE, _('Private')),
        (GROUP, _('Group')),
        (SUPERGROUP, _('Supergroup')),
        (CHANNEL, _('Channel')),
    )

    id = models.BigIntegerField(
        primary_key=True,
        unique=True,
        help_text=_('Unique identifier for this chat.'),
    )
    type = models.CharField(
        max_length=255,
        choices=CHOICES,
        verbose_name=_('Type'),
    )
    title = models.CharField(
        verbose_name=_('title'),
        max_length=255,
        null=True,
        blank=True,
        help_text=_('Title, for supergroups, channels and group chats.'),
    )
    username = models.CharField(
        verbose_name=_('Unique username'),
        max_length=255,
        null=True,
        blank=True,
    )
    first_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_('First name of the other party in a private chat'),
    )
    last_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_('Last name of the other party in a private chat'),
    )
    default_keyboard = models.TextField(
        max_length=1000,
        null=True,
        blank=True,
        verbose_name=_('Chat menu'),
        help_text=_('Chat menu, is used to inherit markup keyboard styles')
    )

    class Meta:
        verbose_name = _('Chat')
        verbose_name_plural = _('Chats')

    def __str__(self):
        """Represent chat name"""
        return str(self.id)

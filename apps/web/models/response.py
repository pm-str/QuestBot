import re

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.web.managers import ResponseManager
from apps.web.models.bot import Bot
from apps.web.models.chat import Chat
from apps.web.models.update import Update
from apps.web.querysets import ResponseQuerySet

from .abstract import TimeStampModel


def username_list(value: str):
    for username in value.split(' '):
        if not re.match('[_a-zA-Z0-9]+', username):
            raise ValidationError(
                _("Username %(username)s is invalid"),
                code='invalid',
                params={'username': username},
            )


class Response(TimeStampModel):
    objects = ResponseQuerySet.as_manager()

    title = models.CharField(verbose_name='Response title', max_length=1000)
    on_true = models.BooleanField(
        verbose_name=_('Triggering on true'),
        default=True,
    )
    as_reply = models.BooleanField(
        verbose_name=_('Send as reply'),
        default=False,
    )
    message = models.TextField(
        max_length=5000,
        verbose_name=_('Message text'),
        null=True,
        blank=True,
    )
    keyboard = models.TextField(
        max_length=2000,
        verbose_name=_('Keyboard layout'),
        null=True,
        blank=True,
    )
    handler = models.ForeignKey(
        verbose_name=_('Attached handler to'),
        to='Handler',
        related_name='responses',
    )
    redirect_to = models.TextField(
        verbose_name=_('Redirect to'),
        max_length=1000,
        help_text=_('List of usernames separated by whitespace'),
        blank=True,
        validators=[username_list]
    )
    priority = models.SmallIntegerField(
        verbose_name=_('Priority in the queue'),
        default=1,
    )

    def __str__(self):
        return self.title

    def send_message(self, bot: Bot, update: Update):
        """Method responsible for answer and and related actions"""

        bot.send_message(
            chat_id=update.get_message().chat.id,
            reply_message=update if self.as_reply else None,
            keyboard=self.keyboard,
            text=self.message,
        )

        for username in self.redirect_to.split(' '):
            chat = Chat.objects.filter(username=username).first()

            if chat:
                bot.send_message(chat_id=chat.id, text=self.message)

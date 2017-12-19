import ast

from django.db import models
from django.utils.translation import ugettext_lazy as _
from jinja2 import Environment
from telegram import (
    ReplyKeyboardHide,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from apps.web.models.bot import Bot
from apps.web.models.chat import Chat
from apps.web.models.update import Update
from apps.web.querysets import ResponseQuerySet
from apps.web.utils import traverse, jinja2_extensions, jinja2_template_context
from apps.web.validators import username_list, jinja2_template

from .abstract import TimeStampModel


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
        validators=[jinja2_template],
        null=True,
        blank=True,
    )
    keyboard = models.TextField(
        max_length=2000,
        verbose_name=_('Keyboard layout'),
        validators=[jinja2_template],
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

    def _create_keyboard_button(self, element):
        if isinstance(element, tuple):
            if element[1].startswith('http'):
                return InlineKeyboardButton(text=element[0], url=element[1])
            else:
                return InlineKeyboardButton(text=element[0],
                                            callback_data=element[1])
        else:
            return InlineKeyboardButton(text=element, callback_data=element)

    def build_keyboard(self, keyboard):
        if keyboard:
            # since jinja2 template represents for list of buttons
            # it should be converted into python object via ast library
            built_keyboard = InlineKeyboardMarkup(
                [[self._create_keyboard_button(element)]
                 for element in traverse(ast.literal_eval(keyboard))]
            )
        else:
            built_keyboard = ReplyKeyboardHide()
        return built_keyboard

    def send_message(self, bot: Bot, update: Update):
        """Method responsible for answer and and related actions"""

        env = Environment(extensions=jinja2_extensions())
        keyboard_template = env.from_string(self.keyboard)
        keyboard = keyboard_template.render(jinja2_template_context())

        message_template = env.from_string(self.message)
        message = message_template.render(jinja2_template_context())

        bot.send_message(
            chat_id=update.get_message().chat.id,
            reply_message=update if self.as_reply else None,
            keyboard=self.build_keyboard(keyboard),
            text=message,
        )

        for username in self.redirect_to.split(' '):
            chat = Chat.objects.filter(username=username).first()

            if chat:
                bot.send_message(chat_id=chat.id, text=self.message)

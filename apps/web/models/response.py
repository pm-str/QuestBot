import ast

from django.db import models
from django.utils.translation import ugettext_lazy as _
from jinja2 import Environment
from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from apps.web.models.bot import Bot
from apps.web.models.chat import Chat
from apps.web.models.update import Update
from apps.web.querysets import ResponseQuerySet
from apps.web.utils import traverse, jinja2_extensions, \
    jinja2_template_context, clear_redundant_tags
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
    inherit_keyboard = models.BooleanField(
        verbose_name=_('Display last used keyboard'),
        default=True,
    )
    set_default_keyboard = models.BooleanField(
        verbose_name=_('Save this keyboard as default for chat'),
        default=False,
    )
    delete_previous_keyboard = models.BooleanField(
        verbose_name=_('Delete previous keyboard'),
        default=False,
    )
    one_time_keyboard = models.BooleanField(
        verbose_name=_('Hide keyboard after click on'),
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
    redirect_to = models.CharField(
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
            return KeyboardButton(text=element[0])

    def build_keyboard(self, keyboard, one_time_keyboard):
        built_keyboard = []

        if keyboard:
            # since jinja2 template represents for list of buttons
            # it should be converted into python object via ast library
            built_keyboard = ReplyKeyboardMarkup(
                [[self._create_keyboard_button(element)]
                 for element in traverse(ast.literal_eval(keyboard))],
                one_time_keyboard=one_time_keyboard,
            )
        return built_keyboard

    def send_message(self, bot: Bot, update: Update):
        """Method responsible for answer and and related actions"""

        chat = update.get_message.chat
        env = Environment(extensions=jinja2_extensions())
        keyboard_template = env.from_string(self.keyboard)
        keyboard = keyboard_template.render(jinja2_template_context())

        if self.inherit_keyboard and chat.default_keyboard:
            keyboard = chat.default_keyboard

        if self.set_default_keyboard:
            chat.default_keyboard = keyboard
            chat.save()

        keyboard = self.build_keyboard(keyboard, self.one_time_keyboard)

        if self.delete_previous_keyboard:
            keyboard = {'hide_keyboard': True}

        message_template = env.from_string(clear_redundant_tags(self.message))
        message = message_template.render(jinja2_template_context())

        bot.send_message(
            chat_id=chat.id,
            reply_message=update if self.as_reply else None,
            keyboard=keyboard,
            text=message,
        )

        for username in self.redirect_to.split(' '):
            chat = Chat.objects.filter(username=username).first()

            if chat:
                bot.send_message(chat_id=chat.id, text=self.message)

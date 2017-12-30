import ast

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from jinja2 import Environment
from telegram import KeyboardButton

from apps.web.models.bot import Bot
from apps.web.models.chat import Chat
from apps.web.models.message import Message
from apps.web.querysets import ResponseQuerySet
from apps.web.tasks import send_message_task
from apps.web.utils import clear_redundant_tags
from apps.web.validators import (
    array_field_validator,
    jinja2_template_validator,
)

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
    text = models.TextField(
        max_length=5000,
        verbose_name=_('Message text'),
        validators=[jinja2_template_validator],
        null=True,
        blank=True,
    )
    keyboard = models.TextField(
        max_length=2000,
        verbose_name=_('Keyboard layout'),
        validators=[array_field_validator],
        null=True,
        blank=True,
    )
    handler = models.ForeignKey(
        verbose_name=_('Attached handler to'),
        to='Handler',
        related_name='responses',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    priority = models.SmallIntegerField(
        verbose_name=_('Priority in the queue'),
        default=1,
    )

    def __str__(self):
        if self.handler:
            step = str(self.handler.step.number)
        else:
            step = 'Undefined'

        return ' | '.join([step, self.title])

    def _create_keyboard_button(self, element):
        if isinstance(element, tuple):
            return KeyboardButton(text=element[0])

    def build_keyboard(self, keyboard, one_time_keyboard):
        built_keyboard = []

        if keyboard:
            # since jinja2 template represents for list of buttons
            # it should be converted into python object via ast library
            built_keyboard = dict(
                keyboard=list(ast.literal_eval(keyboard)),
                one_time_keyboard=one_time_keyboard,
                resize_keyboard=True,
                selective=False,
            )
        return built_keyboard

    @staticmethod
    def render_layout(message, keyboard, context):
        env = Environment(extensions=settings.JINJA2_EXTENTIONS)
        keyboard_template = env.from_string(keyboard)
        keyboard = keyboard_template.render(context)

        message_template = env.from_string(clear_redundant_tags(message))
        message = message_template.render(context)

        return message, keyboard

    def send_response(self, bot: Bot, chat: Chat, message: Message, eta=None):
        """Method responsible for answer and and related actions"""

        text, keyboard = self.render_layout(
            self.text,
            self.keyboard,
            context=chat.template_context,
        )

        if self.inherit_keyboard and chat.default_keyboard:
            keyboard = chat.default_keyboard

        if self.set_default_keyboard:
            chat.default_keyboard = keyboard
            chat.save()

        if self.delete_previous_keyboard:
            keyboard = {'hide_keyboard': True}
            chat.current_keyboard = None
        else:
            keyboard = self.build_keyboard(keyboard, self.one_time_keyboard)
            chat.current_keyboard = keyboard

        # updates chat after keyboard changing
        chat.save()
        send_message_task.apply_async(
            (bot.id,),
            dict(
                chat_id=chat.id,
                reply_message_id=(
                    message.message_id if message and self.as_reply else None
                ),
                keyboard=keyboard,
                text=text,
                disable_notifications=chat.no_notifications,
                disable_links_preview=chat.no_links_preview,
            ),
            eta=eta,
        )

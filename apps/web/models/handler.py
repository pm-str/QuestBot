import re

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.web.conditions_parsing import NumericStringParser
from apps.web.models.constants import HookActions
from apps.web.models.update import Update
from apps.web.tasks import send_message_task
from apps.web.validators import condition_validator

from .abstract import TimeStampModel

REPLY_BUTTON = HookActions.REPLY_BUTTON
MESSAGE = HookActions.MESSAGE
CALLBACK = HookActions.CALLBACK
COMMAND = HookActions.COMMAND

FIELD_CHOICES = (
    (REPLY_BUTTON, _('Reply button')),
    (MESSAGE, _('Message')),
    (COMMAND, _('Command')),
    (CALLBACK, _('Callback')),
)


class Handler(TimeStampModel):
    step = models.ForeignKey(
        to='Step',
        help_text=_('Handle particular actions for this step'),
        related_name='handlers',
        on_delete=models.CASCADE,
    )
    enabled_on = models.CharField(
        verbose_name=_('Enabled on'),
        help_text=_('Enabled only on following requests'),
        max_length=255,
        choices=FIELD_CHOICES,
        default=REPLY_BUTTON,
    )
    ids_expression = models.CharField(
        max_length=500,
        verbose_name='Mathematics expression',
        help_text=_("A set of math symbols to construct a particular rule,"
                    "example: {} + {} > 1; example2: {cond_id} == 0"),
        null=True,
        blank=True,
        validators=[condition_validator]
    )
    step_on_success = models.ForeignKey(
        to='Step',
        verbose_name='Step on success',
        help_text='Move to this step if mathematics expression truthful',
        related_name='true_handlers',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    step_on_error = models.ForeignKey(
        to='Step',
        verbose_name='Step on error',
        help_text='Move to this step if mathematics expression wrongful',
        related_name='false_handlers',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    title = models.CharField(verbose_name="Handler title", max_length=255)
    redirects = models.ManyToManyField(
        to='AppUser',
        verbose_name=_('Redirects'),
        help_text=_('Users the message redirect to'),
        blank=True,
    )

    class Meta:
        verbose_name = _('Handler')
        verbose_name_plural = _('Handlers')

    def __str__(self):
        return ' | '.join([str(self.step.number), self.title, ])

    def redirect_message(self, bot, chat, message):
        for user in list(self.redirects.all()):
            chat = chat.objects.filter(username__iexact=user.username).first()

            fmtd_text = """
            Bot: {bot}\nChat: {chat}\nMessage ID: {message}\nText: {text}\n
            """.format(
                bot=bot,
                chat=chat,
                message=message.message_id if message else None,
                text=message.text if message else None,
            )

            if chat:
                send_message_task(bot.id, chat_id=chat.id, text=fmtd_text)

    def check_handler_conditions(
            self,
            update: Update,
            specify_ids: bool = True,
    ) -> bool:
        """Responsible for conditions checking

        Ensure that massage fits in with the condition rules

        """
        conditions = self.conditions

        if self.ids_expression:
            expr = self.ids_expression.replace(' ', '') + ' '
        elif conditions.count():
            expr = '{}' * conditions.count() + ' '
        else:
            return False

        if not re.match('^.*{\d+}.*$', expr):
            specify_ids = False

        cond_result = {
            ''.join(['#', str(i.id)]): int(i.is_match_to_rule(update))
            for i in self.conditions.all()
        }

        formatted_expr = ''
        for i in range(len(expr)-1):
            formatted_expr += expr[i]
            if specify_ids and expr[i] == '{' and expr[i+1].isdigit():
                formatted_expr += '#'

        if specify_ids:
            filled_expr = formatted_expr.format(**cond_result)
        else:
            filled_expr = formatted_expr.format(*list(cond_result.values()))

        nsp = NumericStringParser()
        result = nsp.eval(filled_expr)

        return bool(result)

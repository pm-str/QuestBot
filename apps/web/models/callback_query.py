from django.db import models
from django.utils.translation import ugettext_lazy as _

from .abstract import TimeStampModel


class CallbackQuery(TimeStampModel):
    id = models.BigIntegerField(
        verbose_name=_('Callback id'),
        primary_key=True,
        unique=True,
    )
    from_user = models.ForeignKey(
        to='AppUser',
        related_name='callback_queries',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    message = models.ForeignKey(
        to='Message',
        related_name='callback_queries',
        verbose_name=_('Message ID'),
        help_text=_(
            'Message with the callback button that originated the query.'
        ),
        on_delete=models.CASCADE,
    )
    data = models.TextField(
        max_length=1000,
        verbose_name=_('Callback data'),
        help_text=_('Data associated with the callback button.'),
    )

    class Meta:
        verbose_name = _('Callback query')
        verbose_name_plural = _('Callback queries')

    def __str__(self):
        return f'{self.id}'

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .abstract import TimeStampModel


class Update(TimeStampModel):
    bot = models.ForeignKey(to='Bot', verbose_name=_('Bot from'))
    update_id = models.BigIntegerField(
        verbose_name=_('Update Id'),
        db_index=True,
    )
    message = models.ForeignKey(
        to='Message',
        related_name='updates',
        verbose_name=_('Message ID'),
        help_text=_('Update action for particular massage')
    )
    callback_query = models.ForeignKey(
        to='CallbackQuery',
        related_name='updates',
        verbose_name=_('Callback Query'),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('Update')
        verbose_name_plural = _('Updates')

    def __str__(self):
        return self.id

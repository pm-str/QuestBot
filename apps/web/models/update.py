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
    handler = models.ForeignKey(
        to='Handler',
        related_name='updates',
        verbose_name='Handler',
        help_text=_('Handler contains expression needed to process a message'),
        blank=True,
        null=True,
    )
    response = models.ForeignKey(
        to='Response',
        related_name='updates',
        verbose_name='Response',
        help_text=_('Response that contain this message'),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Update')
        verbose_name_plural = _('Updates')

    def __str__(self):
        return self.id

    def get_message(self):
        if self.message:
            return self.message
        if self.callback_query:
            return self.callback_query.message
        raise AttributeError

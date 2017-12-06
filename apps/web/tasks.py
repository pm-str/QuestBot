from __future__ import absolute_import, unicode_literals

from celery import shared_task
import time

from apps.web.models import Update


@shared_task
def handle_message(update: Update):
    pass
    # bot = update.bot
    # message = update.message
    # user = message.from_user
    #
    # for step in user.steps:
    #     handlers = step.handlers.filter(allowed=user)
    #
    #     for handler in handlers:
    #         is_true = handler.check_conditions(message=message)
    #         handler.responses.filter(on_true=is_true)



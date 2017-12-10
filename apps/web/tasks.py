from __future__ import absolute_import, unicode_literals

from celery import shared_task

from apps.web.models import AppUser, Bot, Update
from apps.web.models.step import FINISHED, IN_PROCESS


@shared_task
def handle_message(update: Update):
    bot: Bot = update.bot
    user: AppUser = update.message.from_user

    for step in list(user.steps):
        handlers = step.handlers.filter(allowed__contains=user)

        for handler in handlers:
            is_true = handler.check_conditions(update)
            responses = handler.responses.filter(on_true=is_true)

            if is_true:
                next_step = handler.step_on_success
            else:
                next_step = handler.step_on_error

            if next_step:
                next_step.status = IN_PROCESS
                next_step.save()

            user.steps.add(step)
            responses.send_message(bot, update)

            step.status = FINISHED
            step.save()

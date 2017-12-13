from __future__ import absolute_import, unicode_literals

from celery import shared_task

from apps.web.models import AppUser, Bot, Update


@shared_task
def handle_message(update: Update):
    bot: Bot = update.bot
    user: AppUser = update.message.from_user

    if not user.step:
        bot.quest.initialize_user(user)

    step = user.step
    handlers = step.handlers.filter(allowed=user)

    for handler in handlers:
        is_true = handler.check_handler_conditions(update)
        responses = handler.responses.filter(on_true=is_true)

        if is_true:
            next_step = handler.step_on_success
        else:
            next_step = handler.step_on_error

        if next_step:
            user.step = next_step
            user.save()

        responses.send_message(bot, update)


from __future__ import absolute_import, unicode_literals

from celery import shared_task

from apps.web.models.user import AppUser
from apps.web.models.bot import Bot
from apps.web.models.update import Update


@shared_task
def handle_message_task(update_id: int):
    update = Update.objects.get(id=update_id)
    bot: Bot = update.bot
    user: AppUser = update.get_sender
    chat = update.get_message.chat
    message = update.get_message

    if not user.step:
        bot.quest.initialize_user(user)

    step = user.step
    handlers = step.handlers.filter(enabled_on=update.action_type)

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

        responses.send_response(bot, chat, message)


@shared_task
def send_message_task(bot_id, *args, **kwargs):
    """Proxy method wrapped by celery tasks"""

    bot = Bot.objects.get(id=bot_id)
    print(bot_id, args, kwargs)
    bot.send_message(*args, **kwargs)

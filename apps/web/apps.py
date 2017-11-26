from django.apps import AppConfig, apps


def connect_telegram_bot_signals():
    """Inject Telegram bot handlers"""
    import apps.web.signals.handlers


class SignalsConfig(AppConfig):
    """Class that set up signals after models are ready"""

    name = 'apps.web'
    verbose_name = 'TelegramTasks'

    def ready(self):
        connect_telegram_bot_signals()

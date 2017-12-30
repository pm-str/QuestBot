"""This settings configure dynamic variables

These ones can be set up in Django Admin in ``Constance`` section

"""
from telegram import ParseMode

WEBHOOKS_APIVIEW_URL = 'webhooks_apiview_url'
WEBHOOKS_NULL_URL = 'webhooks_null_url'

TELEGRAM_DEFAULT_PASS = 'telegram_default_pass'
TELEGRAM_PARSE_MODE = 'telegram_parse_mode'

CONSTANCE_ADDITIONAL_FIELDS = {
    'parse_mode_select': ['django.forms.fields.ChoiceField', {
        'widget': 'django.forms.Select',
        'choices': ((ParseMode.HTML, "HTML"), (ParseMode.MARKDOWN, "MARKDOWN"))
    }],
}

CONSTANCE_CONFIG = {
    WEBHOOKS_APIVIEW_URL: (
        'web-api:webhook-processing',
        'Url for Telegram webhooks',
        str
    ),
    WEBHOOKS_NULL_URL: (
        'https://example.com',
        'Telegram webhooks url if bot is disabled or ``WEBHOOKS_URL`` empty',
        str,
    ),
    TELEGRAM_DEFAULT_PASS: (
        'Password1!',
        'Default password for new telegram users',
        str,
    ),
    TELEGRAM_PARSE_MODE: (
        ParseMode.HTML,
        'Telegram message format',
        'parse_mode_select',
    ),
}

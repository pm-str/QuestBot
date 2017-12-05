"""This settings configure dynamic variables

These ones can be set up in Django Admin in ``Constance`` section

"""

WEBHOOKS_APIVIEW_URL = 'webhooks_apiview_url'
WEBHOOKS_NULL_URL = 'webhooks_null_url'
TELEGRAM_DEFAULT_PASS = 'telegram_default_pass'

CONSTANCE_CONFIG = {
    'webhooks_apiview_url': (
        'web-api:webhook-processing',
        'Url for Telegram webhooks',
        str
    ),
    'webhooks_null_url': (
        'https://example.com',
        'Telegram webhooks url if bot is disabled or ``WEBHOOKS_URL`` empty',
        str,
    ),
    'telegram_default_pass': (
        'Password1!',
        'Default password for new telegram users',
        str,
    )
}

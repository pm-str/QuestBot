"""This settings configure dynamic variables

These ones can be set up in Django Admin in ``Constance`` section

"""

WEBHOOKS_APIVIEW_URL = 'WEBHOOKS_APIVIEW_URL'
WEBHOOKS_NULL_URL = 'WEBHOOKS_NULL_URL'

CONSTANCE_CONFIG = {
    'WEBHOOKS_APIVIEW_URL': (
        'web-api:webhook-processing',
        'Url for Telegram webhooks',
        str
    ),
    'WEBHOOKS_NULL_URL': (
        'https://example.com',
        'Telegram webhooks url if bot is disabled or ``WEBHOOKS_URL`` empty',
        str,
    ),
}

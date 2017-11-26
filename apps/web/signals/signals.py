from django.dispatch import Signal


update_webhook_signal = Signal(providing_args=['instance'])

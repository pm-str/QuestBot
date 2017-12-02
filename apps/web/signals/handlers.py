import logging

from constance import config
from constance.signals import config_updated
from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse

from apps.web.models.bot import Bot

from .signals import update_webhook_signal

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Site)
@receiver(config_updated)
def dispatcher(sender, instance, *args, **kwargs):
    """Retrieve ``config_updated`` signal from constance

    Check if it was url updating, it should be webhook configured again.

    """

    objects = Bot.objects.all()

    for bot in objects:
        update_webhook_signal.send(sender=Bot, instance=bot)

    logging.debug("Constance's settings have been updated")


@receiver(pre_save, sender=Bot)
def pre_save_bot_handler(sender, instance, *args, **kwargs):
    """Implement ``full_clean`` method call before ``Bot`` instance saving"""

    instance.full_clean()
    update_webhook_signal.send(sender=Bot, instance=instance)


@receiver([update_webhook_signal])
def setup_hooks(sender, instance, *args, **kwargs):
    """Setup telegram hooks based on the url

    Arguments:
        instance (Bot): instance of ``Bot`` model

    """
    url = getattr(config, settings.WEBHOOKS_NULL_URL)

    if not instance.is_initialized:
        instance.init_bot()

    if instance.enabled:
        site_url = Site.objects.get_current().domain
        api_url = reverse(getattr(config, settings.WEBHOOKS_APIVIEW_URL),
                          kwargs={'hook_id': instance.hook_id})
        url = 'https://{site_url}/{api_url}/'.format(
            site_url=site_url.strip('/'),
            api_url=api_url.strip('/'),
        )

    instance.set_webhook(url)
    logging.debug('Set up webhook for Telegram Bot - {}'.format(url))

    # logging.error('Error on webhook setup for Telegram Bot'.format(url))

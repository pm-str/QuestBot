from django.db.models import Manager

from apps.web.querysets import ResponseQuerySet


class ResponseManager(Manager):
    """Custom response manager to create actions upon the bunch of objects"""

    def get_queryset(self):
        return ResponseQuerySet(model=self, using=self._db)

    def send_response(self, bot, update):
        self.get_queryset().order_by('priority').send_response(bot, update)

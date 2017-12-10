from django.db.models import Manager


class ResponseManager(Manager):
    """Custom response manager to create actions upon the bunch of objects"""

    def send_message(self, bot, update):
        self.get_queryset().send_message(bot, update)

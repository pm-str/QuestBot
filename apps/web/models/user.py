from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):
    device_uid = models.CharField(
        null=True,
        blank=True,
        verbose_name="Telegram user's id",
        max_length=255,
    )
    steps = models.ManyToManyField(
        to='Step',
        related_name='users',
        verbose_name="User's level",
        blank=True,
    )

    def __str__(self):
        return self.username

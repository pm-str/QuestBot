# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-06 18:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_auto_20171206_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.TextField(blank=True, max_length=2500, null=True, verbose_name='Message text'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-06 19:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_auto_20171206_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photosize',
            name='message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='web.Message', verbose_name='From message'),
        ),
    ]

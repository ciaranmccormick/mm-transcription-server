# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-14 15:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transcript', '0021_auto_20161114_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='extract',
            name='flag',
            field=models.BooleanField(default=False),
        ),
    ]
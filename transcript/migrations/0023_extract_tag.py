# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-16 15:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transcript', '0022_extract_flag'),
    ]

    operations = [
        migrations.AddField(
            model_name='extract',
            name='tag',
            field=models.CharField(default='', max_length=512),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-16 18:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transcript', '0023_extract_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extract',
            name='tag',
            field=models.CharField(blank=True, max_length=512),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-25 16:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transcript', '0005_document_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='extract',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
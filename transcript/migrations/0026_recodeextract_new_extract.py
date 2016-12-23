# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-23 10:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transcript', '0025_recode_recodeextract'),
    ]

    operations = [
        migrations.AddField(
            model_name='recodeextract',
            name='new_extract',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='new_extracts', to='transcript.Extract'),
            preserve_default=False,
        ),
    ]
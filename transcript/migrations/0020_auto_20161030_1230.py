# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-30 12:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transcript', '0019_iattr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iattr',
            name='extract',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='i_attrs', to='transcript.Extract'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-29 21:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transcript', '0008_auto_20161029_2040'),
    ]

    operations = [
        migrations.CreateModel(
            name='IMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.CharField(choices=[(b'AU', b'Automatic'), (b'MN', b'Manual')], max_length=2)),
                ('extract', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='transcript.Extract')),
            ],
        ),
    ]

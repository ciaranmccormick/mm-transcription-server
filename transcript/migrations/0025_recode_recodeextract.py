# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-19 17:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transcript', '0024_auto_20161116_1855'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recoder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RecodeExtract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extract', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='transcript.Extract')),
                ('recode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transcript.Recode')),
            ],
        ),
    ]

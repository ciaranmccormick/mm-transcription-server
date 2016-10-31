# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-30 11:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transcript', '0016_roleexpectation_rolerelationship'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaceLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=300)),
                ('extract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='transcript.Extract')),
            ],
        ),
        migrations.CreateModel(
            name='PlaceNorm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('norm', models.CharField(max_length=300)),
                ('extract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='norms', to='transcript.Extract')),
            ],
        ),
    ]

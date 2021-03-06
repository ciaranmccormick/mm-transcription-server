# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-30 11:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transcript', '0015_auto_20161029_2213'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoleExpectation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expectation', models.CharField(max_length=300)),
                ('extract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expectations', to='transcript.Extract')),
            ],
        ),
        migrations.CreateModel(
            name='RoleRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relationship', models.CharField(max_length=300)),
                ('extract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relationships', to='transcript.Extract')),
            ],
        ),
    ]

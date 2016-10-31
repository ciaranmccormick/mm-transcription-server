# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-29 21:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transcript', '0009_imode'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purpose',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purpose', models.CharField(max_length=300)),
                ('purposes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transcript.Extract')),
            ],
        ),
        migrations.AlterField(
            model_name='imode',
            name='extract',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='i_mode', to='transcript.Extract'),
        ),
    ]

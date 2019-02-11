# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-11 11:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0012_auto_20190211_1028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='show',
            name='episodes',
        ),
        migrations.AddField(
            model_name='episode',
            name='show',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='App.Show'),
            preserve_default=False,
        ),
    ]

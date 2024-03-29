# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-12 10:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_auto_20190212_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='friend',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='new_follower', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='operation',
            name='operation_belongs_to',
            field=models.CharField(choices=[('movie', 'Movie'), ('show', 'Show'), ('episode', 'Episode'), ('follower', 'Follower')], max_length=30),
        ),
    ]

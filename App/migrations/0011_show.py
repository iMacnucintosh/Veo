# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-11 09:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('App', '0010_auto_20190208_1328'),
    ]

    operations = [
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_show', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('poster_path', models.CharField(max_length=50)),
                ('date_add', models.DateTimeField(auto_now_add=True)),
                ('states', models.ManyToManyField(blank=True, to='App.State')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

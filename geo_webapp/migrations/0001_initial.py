# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-31 09:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SearchTown',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zeitstempel', models.DateTimeField()),
                ('text', models.TextField(verbose_name='eingegebene Suche')),
            ],
        ),
    ]
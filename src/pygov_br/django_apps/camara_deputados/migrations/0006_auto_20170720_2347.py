# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-20 23:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('camara_deputados', '0005_auto_20170719_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='proposals', to='camara_deputados.Deputy'),
        ),
    ]
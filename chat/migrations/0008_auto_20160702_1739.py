# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-02 22:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_auto_20160702_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensaje',
            name='mensaje_contenido',
            field=models.TextField(),
        ),
    ]
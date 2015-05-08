# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('centre_registry', '0003_auto_20150223_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='email_address',
            field=models.EmailField(max_length=254, verbose_name='E-mail address'),
        ),
    ]

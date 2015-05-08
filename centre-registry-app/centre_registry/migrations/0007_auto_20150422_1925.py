# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('centre_registry', '0006_auto_20150422_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='samlserviceprovider',
            name='production_status',
            field=models.BooleanField(default=True, verbose_name='Has production status?'),
        ),
    ]

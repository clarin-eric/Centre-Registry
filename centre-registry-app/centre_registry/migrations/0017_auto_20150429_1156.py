# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('centre_registry', '0016_auto_20150428_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consortium',
            name='website_url',
            field=models.URLField(blank=True, verbose_name='Website URL', max_length=2000),
        ),
    ]

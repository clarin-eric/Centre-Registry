# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('centre_registry', '0010_auto_20150424_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='website_url',
            field=models.URLField(verbose_name='Website URL', blank=True, max_length=2000),
        ),
    ]

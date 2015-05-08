# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('centre_registry', '0009_auto_20150423_1526'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='website',
            new_name='website_url',
        ),
    ]

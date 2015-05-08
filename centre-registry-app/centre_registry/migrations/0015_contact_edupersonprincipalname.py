# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('centre_registry', '0014_remove_contact_edupersonprincipalname'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='edupersonprincipalname',
            field=models.CharField(null=True, verbose_name='eduPersonPrincipalName', blank=True, unique=True, max_length=100),
        ),
    ]

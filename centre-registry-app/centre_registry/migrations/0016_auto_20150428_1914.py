# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('centre_registry', '0015_contact_edupersonprincipalname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='samlidentityfederation',
            name='saml_sps_registered',
        ),
        migrations.AddField(
            model_name='samlidentityfederation',
            name='signing_key',
            field=models.TextField(verbose_name='XML digital signature X.509v3 public key (PEM format)', blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('centre_registry', '0011_auto_20150424_1336'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='centre',
            options={'verbose_name': 'centre', 'verbose_name_plural': 'centres', 'ordering': ('shorthand',)},
        ),
        migrations.AlterModelOptions(
            name='centretype',
            options={'verbose_name': 'centre type', 'verbose_name_plural': 'centre types', 'ordering': ('type',)},
        ),
        migrations.AlterModelOptions(
            name='samlidentityfederation',
            options={'verbose_name': 'SAML identity federation', 'verbose_name_plural': 'SAML identity federations', 'ordering': ('shorthand',)},
        ),
        migrations.AlterField(
            model_name='oaipmhendpoint',
            name='metadata_format',
            field=models.ForeignKey(verbose_name='Metadata format (historic artifact)', to='centre_registry.MetadataFormat'),
        ),
    ]

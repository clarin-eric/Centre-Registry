# Generated by Django 2.2.8 on 2020-02-07 17:29

import centre_registry.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('centre_registry', '0025_auto_20200122_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='oaipmhendpoint',
            name='uri_list',
            field=centre_registry.models.StringListField(blank=True, verbose_name='List of base URIs'),
        ),
    ]

# pylint: disable=invalid-name
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [('centre_registry', '0017_auto_20150429_1156'), ]

    operations = [
        migrations.AlterField(
            model_name='consortium',
            name='alias',
            field=models.CharField(
                blank=True,
                max_length=25,
                verbose_name='DNS subdomain alias * (*.clarin.eu)'), ),
        migrations.AlterField(
            model_name='samlidentityfederation',
            name='signing_key',
            field=models.TextField(
                blank=True,
                verbose_name='XML digital signature X.509v3 public key '
                '(PEM format, without '
                '"-----BEGIN CERTIFICATE-----" begin and and end '
                'marker)'), ),
    ]

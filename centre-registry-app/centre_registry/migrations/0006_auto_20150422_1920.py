# pylint: disable=invalid-name
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [('centre_registry', '0005_auto_20150422_1913'), ]

    operations = [
        migrations.AlterField(
            model_name='oaipmhendpoint',
            name='web_services_set',
            field=models.CharField(
                blank=True,
                max_length=100,
                verbose_name='Web services set (historic artifact)'), ),
        migrations.AlterField(
            model_name='oaipmhendpoint',
            name='web_services_type',
            field=models.CharField(
                default='REST',
                max_length=8,
                verbose_name='Web services type (historic artifact)',
                choices=[('REST', 'REST'), ('SOAP', 'SOAP'),
                         ('WebLicht', 'WebLicht')]), ),
    ]

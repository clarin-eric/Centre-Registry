# pylint: disable=invalid-name
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [('centre_registry', '0007_auto_20150422_1925'), ]

    operations = [
        migrations.AlterModelOptions(
            name='fcsendpoint',
            options={'verbose_name_plural': 'FCS endpoints',
                     'ordering': ('uri', ),
                     'verbose_name': 'FCS endpoint'}, ),
        migrations.AlterModelOptions(
            name='oaipmhendpoint',
            options={'verbose_name_plural': 'OAI-PMH endpoints',
                     'ordering': ('uri', ),
                     'verbose_name': 'OAI-PMH endpoint'}, ),
        migrations.AlterModelOptions(
            name='samlserviceprovider',
            options={'verbose_name_plural': 'SAML Service Providers',
                     'ordering': ('entity_id', ),
                     'verbose_name': 'SAML Service Provider'}, ),
        migrations.AlterModelOptions(
            name='urlreference',
            options={'verbose_name_plural': 'URL references',
                     'ordering': ('centre', ),
                     'verbose_name': 'URL reference'}, ),
    ]

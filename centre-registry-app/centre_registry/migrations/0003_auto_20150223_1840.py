# pylint: disable=invalid-name
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [('centre_registry', '0002_auto_20141128_1731'), ]

    operations = [
        migrations.AlterModelOptions(name='centre',
                                     options={'ordering':
                                              ('administrative_contact',
                                               'technical_contact'),
                                              'verbose_name_plural': 'centres',
                                              'verbose_name': 'centre'}, ),
        migrations.AlterModelOptions(
            name='centretype',
            options={'ordering': ('type', ),
                     'verbose_name_plural': 'formal centre types',
                     'verbose_name': 'formal centre type'}, ),
        migrations.AlterModelOptions(
            name='consortium',
            options={'ordering': ('country_code', 'country_name', 'name'),
                     'verbose_name_plural': 'consortia',
                     'verbose_name': 'consortium'}, ),
        migrations.AlterModelOptions(name='contact',
                                     options={'ordering': ('name', ),
                                              'verbose_name_plural':
                                              'contacts',
                                              'verbose_name': 'contact'}, ),
        migrations.AlterModelOptions(
            name='metadataformat',
            options={'ordering': ('name', ),
                     'verbose_name_plural': 'metadata formats',
                     'verbose_name': 'metadata format'}, ),
        migrations.AlterModelOptions(
            name='samlidentityfederation',
            options={'ordering': ('shorthand', ),
                     'verbose_name_plural': 'SAML Identity Federations',
                     'verbose_name': 'SAML Identity Federation'}, ),
        migrations.AddField(model_name='centre',
                            name='monitoring_contacts',
                            field=models.ManyToManyField(
                                blank=True,
                                related_name='monitoring_contacts',
                                to='centre_registry.Contact'),
                            preserve_default=True, ),
        migrations.AddField(model_name='contact',
                            name='edupersonprincipalname',
                            field=models.CharField(
                                max_length=100,
                                blank=True,
                                verbose_name='eduPersonPrincipalName'),
                            preserve_default=True, ),
        migrations.AlterField(model_name='centre',
                              name='type',
                              field=models.ManyToManyField(
                                  verbose_name='Type',
                                  to='centre_registry.CentreType'),
                              preserve_default=True, ),
        migrations.AlterField(model_name='contact',
                              name='name',
                              field=models.CharField(max_length=100,
                                                     verbose_name='Name'),
                              preserve_default=True, ),
    ]

# pylint: disable=invalid-name
import centre_registry.models
from django.db import migrations
from django.db import models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Centre',
            fields=[
                ('id', models.AutoField(
                    serialize=False,
                    primary_key=True,
                    auto_created=True,
                    verbose_name='ID')),
                ('name', models.CharField(
                    max_length=200, unique=True, verbose_name='Name')),
                ('shorthand', models.CharField(
                    max_length=20, unique=True,
                    verbose_name='Shorthand code')),
                ('organisation_name', models.CharField(
                    max_length=100, verbose_name='Organisation')),
                ('institution', models.CharField(
                    max_length=200, verbose_name='Institution')),
                ('working_unit', models.CharField(
                    max_length=200, verbose_name='Working unit')),
                ('address', models.CharField(
                    max_length=100, verbose_name='Address')),
                ('postal_code', models.CharField(
                    max_length=8, verbose_name='Postal code')),
                ('city', models.CharField(
                    max_length=100, verbose_name='City')),
                ('latitude', models.CharField(
                    max_length=20,
                    validators=[centre_registry.models.validate_latitude],
                    verbose_name='Latitude')),
                ('longitude', models.CharField(
                    max_length=20,
                    validators=[centre_registry.models.validate_longitude],
                    verbose_name='Longitude')),
                ('type_status', models.CharField(
                    max_length=100,
                    blank=True,
                    verbose_name="Comments about centre's type")),
                ('website_url', models.URLField(
                    max_length=2000, verbose_name='Website URL')),
                ('description', models.CharField(
                    max_length=500, blank=True, verbose_name='Description')),
                ('expertise', models.CharField(
                    max_length=200, blank=True, verbose_name='Expertise')),
                ('type_certificate_url', models.URLField(
                    max_length=2000,
                    blank=True,
                    verbose_name='Centre type certificate URL')),
                ('dsa_url', models.URLField(
                    max_length=2000,
                    blank=True,
                    verbose_name='Data Seal of Approval URL')),
                ('pid_status', models.CharField(
                    max_length=200,
                    blank=True,
                    verbose_name='Persistent Identifier usage status')),
                ('long_term_archiving_policy', models.CharField(
                    max_length=200,
                    blank=True,
                    verbose_name='Long Time Archiving Policy')),
                ('repository_system', models.CharField(
                    max_length=200,
                    blank=True,
                    verbose_name='Repository system')),
                ('strict_versioning', models.BooleanField(
                    default=False, verbose_name='Strict versioning?')),
            ],
            options={
                'verbose_name_plural': 'centres',
                'verbose_name': 'centre',
            },
            bases=(models.Model, ), ),
        migrations.CreateModel(
            name='CentreType',
            fields=[
                ('id', models.AutoField(
                    serialize=False,
                    primary_key=True,
                    auto_created=True,
                    verbose_name='ID')),
                ('type', models.CharField(
                    max_length=1,
                    unique=True,
                    verbose_name='Certified centre type')),
            ],
            options={
                'verbose_name_plural': 'formal centre types',
                'verbose_name': 'formal centre type',
            },
            bases=(models.Model, ), ),
        migrations.CreateModel(
            name='Consortium',
            fields=[
                ('id', models.AutoField(
                    serialize=False,
                    primary_key=True,
                    auto_created=True,
                    verbose_name='ID')),
                ('country_code', models.CharField(
                    max_length=3, unique=True, verbose_name='Country code')),
                ('country_name', models.CharField(
                    max_length=20, unique=True, verbose_name='Country name')),
                ('is_observer', models.BooleanField(
                    default=False, verbose_name='Is observer (not member)?')),
                ('name', models.CharField(
                    max_length=20, verbose_name='Name')),
                ('website_url', models.URLField(
                    max_length=2000, verbose_name='Website URL')),
                ('alias', models.CharField(
                    max_length=25, verbose_name='Alias (... .clarin.eu)')),
            ],
            options={
                'verbose_name_plural': 'consortia',
                'verbose_name': 'consortium',
            },
            bases=(models.Model, ), ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(
                    serialize=False,
                    primary_key=True,
                    auto_created=True,
                    verbose_name='ID')),
                ('email_address', models.EmailField(
                    max_length=75, verbose_name='E-mail address')),
                ('name', models.CharField(
                    max_length=200, unique=True, verbose_name='Name')),
                ('telephone_number', models.CharField(
                    max_length=30,
                    blank=True,
                    verbose_name='Telephone number (E.123 international '
                    'notation)')),
                ('website', models.URLField(
                    max_length=2000, blank=True, verbose_name='Website')),
            ],
            options={
                'verbose_name_plural': 'contacts',
                'verbose_name': 'contact',
            },
            bases=(models.Model, ), ),
        migrations.CreateModel(
            name='FCSEndpoint',
            fields=[
                ('id', models.AutoField(
                    serialize=False,
                    primary_key=True,
                    auto_created=True,
                    verbose_name='ID')),
                ('uri', models.URLField(
                    max_length=2000, unique=True, verbose_name='Base URI')),
                ('centre', models.ForeignKey(to='centre_registry.Centre', on_delete=django.db.models.deletion.SET_NULL,
                                             null=True)),
            ],
            options={
                'verbose_name_plural': 'FCS endpoints',
                'verbose_name': 'FCS endpoint',
            },
            bases=(models.Model, ), ),
        migrations.CreateModel(
            name='MetadataFormat',
            fields=[
                ('id', models.AutoField(
                    serialize=False,
                    primary_key=True,
                    auto_created=True,
                    verbose_name='ID')),
                ('name', models.CharField(
                    max_length=30,
                    unique=True,
                    verbose_name='Metadata format name')),
            ],
            options={
                'verbose_name_plural': 'metadata formats',
                'verbose_name': 'metadata format',
            },
            bases=(models.Model, ), ),
        migrations.CreateModel(
            name='OAIPMHEndpoint',
            fields=[
                ('id', models.AutoField(
                    serialize=False,
                    primary_key=True,
                    auto_created=True,
                    verbose_name='ID')),
                ('web_services_set', models.CharField(
                    max_length=100,
                    blank=True,
                    verbose_name='Web services set')),
                ('web_services_type', models.CharField(
                    max_length=10,
                    blank=True,
                    verbose_name='Web services type (e.g. SOAP; REST)')),
                ('uri', models.URLField(
                    max_length=2000, unique=True, verbose_name='Base URI')),
                ('centre', models.ForeignKey(
                    to='centre_registry.Centre',
                    on_delete=django.db.models.deletion.SET_NULL, null=True)),
                ('metadata_format', models.ForeignKey(
                    to='centre_registry.MetadataFormat',
                    verbose_name='Metadata format',
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'verbose_name_plural': 'OAI-PMH endpoints',
                'verbose_name': 'OAI-PMH endpoint',
            },
            bases=(models.Model, ), ),
        migrations.CreateModel(
            name='SAMLIdentityFederation',
            fields=[
                ('id', models.AutoField(
                    serialize=False,
                    primary_key=True,
                    auto_created=True,
                    verbose_name='ID')),
                ('shorthand', models.CharField(
                    max_length=20, unique=True,
                    verbose_name='Shorthand code')),
                ('information_url', models.URLField(
                    max_length=1024, verbose_name='Information URL')),
                ('saml_metadata_url', models.URLField(
                    max_length=1024, verbose_name='SAML metadata URL')),
            ],
            options={
                'verbose_name_plural': 'SAML Identity Federations',
                'verbose_name': 'SAML Identity Federation',
            },
            bases=(models.Model, ), ),
        migrations.CreateModel(
            name='SAMLServiceProvider',
            fields=[
                ('id', models.AutoField(
                    serialize=False,
                    primary_key=True,
                    auto_created=True,
                    verbose_name='ID')),
                ('entity_id', models.URLField(
                    max_length=1024, unique=True, verbose_name='Entity ID')),
                ('status_url', models.URLField(
                    max_length=1024, blank=True, verbose_name='Status URL')),
                ('centre', models.ForeignKey(
                    to='centre_registry.Centre',
                    on_delete=django.db.models.deletion.SET_NULL, null=True)),
            ],
            options={
                'verbose_name_plural': 'SAML Service Providers',
                'verbose_name': 'SAML Service Provider',
            },
            bases=(models.Model, ), ),
        migrations.CreateModel(
            name='URLReference',
            fields=[
                ('id', models.AutoField(
                    serialize=False,
                    primary_key=True,
                    auto_created=True,
                    verbose_name='ID')),
                ('description', models.CharField(
                    max_length=300, verbose_name='Content description')),
                ('url', models.URLField(
                    max_length=2000, unique=True, verbose_name='URL')),
                ('centre', models.ForeignKey(
                    to='centre_registry.Centre',
                    on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'verbose_name_plural': 'URL references',
                'verbose_name': 'URL reference',
            },
            bases=(models.Model, ), ),
        migrations.AddField(
            model_name='samlidentityfederation',
            name='saml_sps_registered',
            field=models.ManyToManyField(
                to='centre_registry.SAMLServiceProvider',
                blank=True,
                verbose_name='SAML SPs Registered'),
            preserve_default=True, ),
        migrations.AddField(
            model_name='centre',
            name='administrative_contact',
            field=models.ForeignKey(
                related_name='administrative_contact',
                to='centre_registry.Contact',
                on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True, ),
        migrations.AddField(
            model_name='centre',
            name='consortium',
            field=models.ForeignKey(
                to='centre_registry.Consortium',
                on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True, ),
        migrations.AddField(
            model_name='centre',
            name='technical_contact',
            field=models.ForeignKey(
                related_name='technical_contact',
                to='centre_registry.Contact',
                on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True, ),
        migrations.AddField(
            model_name='centre',
            name='type',
            field=models.ManyToManyField(to='centre_registry.CentreType'),
            preserve_default=True, ),
    ]

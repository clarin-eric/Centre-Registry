# Generated by Django 5.0 on 2023-12-11 14:19

import centre_registry.models
import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centre_registry', '0036_kcentres_db_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kcentre',
            name='status_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kcentre_status', to='centre_registry.kcentrestatus'),
        ),
        migrations.AlterField(
            model_name='kcentrestatus',
            name='status',
            field=models.CharField(max_length=100, verbose_name='Status'),
        ),
        migrations.CreateModel(
            name='ShadowContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_address', models.EmailField(max_length=254, verbose_name='E-mail address')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('edupersonprincipalname', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='eduPersonPrincipalName')),
                ('telephone_number', models.CharField(blank=True, max_length=40, verbose_name='Telephone number (E.123 international notation)')),
                ('website_url', models.URLField(blank=True, max_length=2000, verbose_name='Website URL')),
                ('contact_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shadow_contact', to='centre_registry.contact')),
            ],
            options={
                'verbose_name': 'Shadow Contact',
                'verbose_name_plural': 'Shadow Contacts',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ShadowCentre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Name')),
                ('shorthand', models.CharField(max_length=30, unique=True, verbose_name='Shorthand code')),
                ('organisation_name', models.CharField(max_length=100, verbose_name='Organisation')),
                ('institution', models.CharField(max_length=200, verbose_name='Institution')),
                ('working_unit', models.CharField(max_length=200, verbose_name='Working unit')),
                ('address', models.CharField(max_length=100, verbose_name='Address')),
                ('postal_code', models.CharField(max_length=20, verbose_name='Postal code')),
                ('city', models.CharField(max_length=100, verbose_name='City')),
                ('latitude', models.CharField(max_length=20, validators=[centre_registry.models.validate_latitude], verbose_name='Latitude (from e.g. Google Maps)')),
                ('longitude', models.CharField(max_length=20, validators=[centre_registry.models.validate_longitude], verbose_name='Longitude (from e.g. Google Maps)')),
                ('type_status', models.CharField(blank=True, max_length=100, verbose_name="Comments about centre's type")),
                ('website_url', models.URLField(max_length=2000, verbose_name='Website URL')),
                ('description', models.CharField(blank=True, max_length=500, verbose_name='Description')),
                ('expertise', models.CharField(blank=True, max_length=200, verbose_name='Expertise')),
                ('type_certificate_url', models.URLField(blank=True, max_length=2000, verbose_name='Centre type certificate URL')),
                ('dsa_url', models.URLField(blank=True, max_length=2000, verbose_name='Data Seal of Approval URL')),
                ('pid_status', models.CharField(blank=True, max_length=200, verbose_name='Persistent Identifier usage status')),
                ('long_term_archiving_policy', models.CharField(blank=True, max_length=200, verbose_name='Long Time Archiving Policy')),
                ('repository_system', models.CharField(blank=True, max_length=200, verbose_name='Repository system')),
                ('strict_versioning', models.BooleanField(default=False, verbose_name='Strict versioning?')),
                ('assessmentdates', models.ManyToManyField(blank=True, related_name='shadow_centre', to='centre_registry.assessmentdates')),
                ('centre_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shadow_centre', to='centre_registry.centre')),
                ('consortium', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='centre_registry.consortium')),
                ('type', models.ManyToManyField(to='centre_registry.centretype', verbose_name='Type')),
                ('shadow_administrative_contact_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shadow_administrative_contact', to='centre_registry.shadowcontact')),
                ('shadow_monitoring_contacts_fks', models.ManyToManyField(blank=True, null=True, related_name='shadow_monitoring_contacts', to='centre_registry.shadowcontact')),
                ('shadow_technical_contact_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shadow_technical_contact', to='centre_registry.shadowcontact')),
            ],
            options={
                'verbose_name': 'centre',
                'verbose_name_plural': 'centres',
                'ordering': ('shorthand',),
            },
        ),
        migrations.CreateModel(
            name='ShadowKCentreServiceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type', models.CharField(max_length=200, unique=True, verbose_name='KCentre service type')),
                ('service_type_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shadow_centre', to='centre_registry.kcentreservicetype')),
            ],
            options={
                'verbose_name': 'Shadow Service type',
                'verbose_name_plural': 'Shadow Service types',
            },
        ),
        migrations.CreateModel(
            name='ShadowKCentreStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100, verbose_name='Status')),
                ('status_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shadow_status', to='centre_registry.kcentrestatus')),
            ],
            options={
                'verbose_name': 'Shadow KCentre status',
                'verbose_name_plural': 'Shadow KCentre statuses',
            },
        ),
        migrations.CreateModel(
            name='ShadowOrganisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organisation_name', models.CharField(max_length=100, verbose_name='Organisation')),
                ('institution', models.CharField(blank=True, max_length=200, verbose_name='Institution')),
                ('working_unit', models.CharField(blank=True, max_length=200, verbose_name='Working unit')),
                ('address', models.CharField(max_length=100, verbose_name='Address')),
                ('postal_code', models.CharField(max_length=20, verbose_name='Postal code')),
                ('city', models.CharField(max_length=100, verbose_name='City')),
                ('latitude', models.CharField(max_length=20, validators=[centre_registry.models.validate_latitude], verbose_name='Latitude (from e.g. Google Maps)')),
                ('longitude', models.CharField(max_length=20, validators=[centre_registry.models.validate_longitude], verbose_name='Longitude (from e.g. Google Maps)')),
                ('organisation_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shadow_organisation', to='centre_registry.organisation')),
            ],
            options={
                'verbose_name': 'Shadow Organisation',
                'verbose_name_plural': 'Shadow Organisations',
                'ordering': ('organisation_name',),
            },
        ),
        migrations.CreateModel(
            name='ShadowKCentre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('published', models.BooleanField(default=False)),
                ('audiences', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(), size=None, verbose_name='Audience list')),
                ('competence', models.CharField(max_length=2000, verbose_name='Competence description')),
                ('data_types', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(), size=None, verbose_name='Data types')),
                ('generic_topics', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(), size=None, verbose_name='Generic topics')),
                ('keywords', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(), size=None, verbose_name='Keywords')),
                ('language_processing_spec', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(), size=None, verbose_name='Language processing specifics')),
                ('languages_processed', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(), size=None, verbose_name='Languages processed')),
                ('linguistic_topics', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(), size=None, verbose_name='Linguistic topics')),
                ('modalities', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(), size=None, verbose_name='Modalities')),
                ('pid', models.URLField(unique=True, verbose_name='PID')),
                ('tour_de_clarin_interview', models.URLField(verbose_name='TdC interview URL')),
                ('tour_de_clarin_intro', models.URLField(verbose_name='TdC intro URL')),
                ('website_language', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(), size=None, verbose_name='Website language')),
                ('resource_families_fks', models.ManyToManyField(related_name='shadow_kcentre', to='centre_registry.resourcefamily')),
                ('shadow_centre_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shadow_kcentre', to='centre_registry.shadowcentre')),
                ('shadow_kcentre_service_type_fks', models.ManyToManyField(related_name='shadow_kcentre', to='centre_registry.shadowkcentreservicetype')),
                ('shadow_kcentre_status_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shadow_kcentre', to='centre_registry.shadowkcentrestatus')),
                ('shadow_secondary_hosts_fks', models.ManyToManyField(blank=True, null=True, related_name='shadow_kcentres', to='centre_registry.shadoworganisation')),
            ],
            options={
                'verbose_name': 'Shadow k-centre',
                'verbose_name_plural': 'Shadow k-centres',
            },
        ),
        migrations.AddField(
            model_name='shadowcentre',
            name='shadow_organisation_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shadow_centre', to='centre_registry.shadoworganisation'),
        ),
    ]

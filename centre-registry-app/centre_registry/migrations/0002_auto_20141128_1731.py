# pylint: disable=invalid-name
import centre_registry.models
from django.db import migrations
from django.db import models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [('centre_registry', '0001_initial'), ]

    operations = [
        migrations.AlterField(
            model_name='centre',
            name='consortium',
            field=models.ForeignKey(
                blank=True, to='centre_registry.Consortium', null=True,
                on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True, ),
        migrations.AlterField(
            model_name='centre',
            name='latitude',
            field=models.CharField(
                max_length=20,
                verbose_name='Latitude (from e.g. Google Maps)',
                validators=[centre_registry.models.validate_latitude]),
            preserve_default=True, ),
        migrations.AlterField(
            model_name='centre',
            name='longitude',
            field=models.CharField(
                max_length=20,
                verbose_name='Longitude (from e.g. Google Maps)',
                validators=[centre_registry.models.validate_longitude]),
            preserve_default=True, ),
        migrations.AlterField(
            model_name='centre',
            name='postal_code',
            field=models.CharField(
                max_length=20, verbose_name='Postal code'),
            preserve_default=True, ),
        migrations.AlterField(
            model_name='centre',
            name='shorthand',
            field=models.CharField(
                max_length=30, verbose_name='Shorthand code', unique=True),
            preserve_default=True, ),
        migrations.AlterField(
            model_name='consortium',
            name='alias',
            field=models.CharField(
                blank=True,
                max_length=25,
                verbose_name='Alias (... .clarin.eu)'),
            preserve_default=True, ),
        migrations.AlterField(
            model_name='consortium',
            name='name',
            field=models.CharField(
                max_length=40, verbose_name='Name'),
            preserve_default=True, ),
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(
                max_length=100, verbose_name='Name', unique=True),
            preserve_default=True, ),
        migrations.AlterField(
            model_name='contact',
            name='telephone_number',
            field=models.CharField(
                blank=True,
                max_length=40,
                verbose_name='Telephone number (E.123 international '
                'notation)'),
            preserve_default=True, ),
        migrations.AlterField(
            model_name='oaipmhendpoint',
            name='web_services_type',
            field=models.CharField(
                blank=True,
                max_length=20,
                verbose_name='Web services type (e.g. SOAP; REST)'),
            preserve_default=True, ),
        migrations.AlterField(
            model_name='samlidentityfederation',
            name='shorthand',
            field=models.CharField(
                max_length=30, verbose_name='Shorthand code', unique=True),
            preserve_default=True, ),
        migrations.AlterField(
            model_name='samlserviceprovider',
            name='entity_id',
            field=models.CharField(
                max_length=1024, verbose_name='Entity ID', unique=True),
            preserve_default=True, ),
    ]

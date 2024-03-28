# Generated by Django 4.2.9 on 2024-01-22 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centre_registry', '0034_populate_organisations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='centre',
            name='organisation_name',
            field=models.CharField(blank=True, max_length=100, verbose_name='Organisation'),
        ),
        migrations.AlterField(
            model_name='centre',
            name='type',
            field=models.ManyToManyField(related_name='centres_of_type', to='centre_registry.centretype', verbose_name='Type'),
        ),
    ]

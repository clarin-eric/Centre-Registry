# Generated by Django 2.2.8 on 2020-01-22 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('centre_registry', '0024_auto_20200122_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oaipmhendpoint',
            name='centre',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='centre_registry.Centre'),
        ),
    ]

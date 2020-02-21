# Generated by Django 2.2.8 on 2020-02-20 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centre_registry', '0031_webservice_populate'),
    ]

    operations = [
        migrations.AddField(
            model_name='oaipmhendpoint',
            name='web_services',
            field=models.ManyToManyField(blank=True, related_name='web_services', to='centre_registry.WebService'),
        ),
    ]

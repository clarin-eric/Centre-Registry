# Generated by Django 2.2.8 on 2020-02-18 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centre_registry', '0028_remove_oaipmhendpoint_web_services_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oaipmhendpoint',
            name='web_services_set',
            field=models.CharField(help_text='Each URI should start from new line', max_length=1024, null=True, verbose_name='List of base URIs'),
        ),
    ]

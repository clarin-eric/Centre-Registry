# Generated by Django 2.2.8 on 2020-02-18 12:28

from django.db import migrations, models

from centre_registry.models import OAIPMHEndpoint, WebService


def populate_web_service(apps, schema_editor):
    unique_web_services = {_web_service[0] for _web_service in
                           list(OAIPMHEndpoint.objects.values_list("web_services_set").distinct())}
    if '' in unique_web_services:
        unique_web_services.remove('')
    for unique_web_service in unique_web_services:
        web_service = WebService(web_service=unique_web_service)
        web_service.save()


class Migration(migrations.Migration):

    dependencies = [
        ('centre_registry', '0030_webservice'),
    ]

    operations = [
        migrations.RunPython(populate_web_service)
    ]

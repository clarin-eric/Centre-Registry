# Generated by Django 2.2.8 on 2020-02-20 11:42

from django.db import migrations, models

from centre_registry.models import OAIPMHEndpoint, WebService


def endpoint_webserviceset_to_fk(apps, schema_editor):
    for endpoint in OAIPMHEndpoint.objects.all():
        webservice = WebService.objects.get(web_service=endpoint.web_services_set)
        endpoint.web_services.add(webservice)
        endpoint.web_services_set = None
        endpoint.save()


class Migration(migrations.Migration):

    dependencies = [
        ('centre_registry', '0032_oaipmhendpoint_web_services'),
    ]

    operations = [
        migrations.RunPython(endpoint_webserviceset_to_fk)
    ]
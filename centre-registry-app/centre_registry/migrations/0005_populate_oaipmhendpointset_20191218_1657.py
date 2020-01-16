# Generated by Django 2.2.8 on 2019-12-18 16:57

from django.db import migrations


def populate_OAIPMHEndpointSet(apps, schema_editor):
    print("HERE!!")
    OAIPMHEndpoint = apps.get_model('centre_registry', 'OAIPMHEndpoint')
    OAIPMHEndpointSet = apps.get_model('centre_registry', 'OAIPMHEndpointSet')

    for endpoint in OAIPMHEndpoint.objects.all():
        endpoint_set_queryset = OAIPMHEndpointSet.objects.filter(centre=endpoint.centre)
        if endpoint_set_queryset.exists():
            endpoint_set = OAIPMHEndpointSet.objects.get(centre=endpoint.centre)
            endpoint_set.oaipmh_endpoints.add(endpoint)
            endpoint_set.save()
        else:
            endpoint_set = OAIPMHEndpointSet(centre=endpoint.centre)
            endpoint_set.save()
            endpoint_set.oaipmh_endpoints.add(endpoint)
            endpoint_set.save()


def reverse_populate_OAIPMHEndpointSet(apps, schema_editor):
    OAIPMHEndpointSet = apps.get_model('centre_registry', 'OAIPMHEndpointSet')
    for endpoint_set in OAIPMHEndpointSet.objects.all():
        for endpoint in endpoint_set.oaipmh_endpoints.all():
            endpoint.centre = endpoint_set.centre
            endpoint.save()
            endpoint_set.oaipmh_endpoints.remove(endpoint)
            endpoint_set.save()
        endpoint_set.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('centre_registry', '0004_oaipmhendpointset_20191218_1532'),
    ]

    operations = [
        migrations.RunPython(populate_OAIPMHEndpointSet, reverse_code=reverse_populate_OAIPMHEndpointSet),
    ]

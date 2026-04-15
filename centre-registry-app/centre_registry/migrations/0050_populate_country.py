

from django.db import migrations


def forwards(apps, schema_editor):
    # CentreModel and OrganisationModel are classes, therefore CamelCase
    ConsortiumModel = apps.get_model("centre_registry", "Consortium")
    for consortium_object in ConsortiumModel.objects.all():
        if consortium_object.country_code:
            country_code = consortium_object.country_code.strip().upper()
            consortium_object.country = country_code
            consortium_object.consortiums_centre.country = consortium_object.country_code
            consortium_object.save()

            consortium_object.consortiums_centre.all().update(country=consortium_object.country_code)


class Migration(migrations.Migration):
    dependencies = [
        ('centre_registry', '0049_alter_centre_consortium'),
    ]

    operations = [
        migrations.RunPython(forwards, reverse_code=migrations.RunPython.noop)
    ]

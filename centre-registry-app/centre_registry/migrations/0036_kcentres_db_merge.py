from django.db import migrations, models
import django.db.models.deletion
import djangoarrayfield.fields
import djangoarrayfield.serializers

import pandas


def forwards(apps, schema_editor):
    CentreModel = apps.get_model("centre_registry", "Centre")
    KCentreModel = apps.get_model("centre_registry", "KCentre")
    KCentreServiceTypeModel = apps.get_model("centre_registry", "KCentreServiceType")
    KCentreStatusModel = apps.get_model("centre_registry", "KCentreStatus")
    ResourceFamilyModel = apps.get_model("centre_registry", "ResourceFamily")
    SEP = ';\n'

    kcentres_df = pandas.read_csv("/home/gawor/Documents/clarin_projects/Centre-Registry/kcentres.csv", sep='#')
    kcentres_df = kcentres_df.fillna('')
    for _, row in kcentres_df.iterrows():
        service_types_strs = row["ServiceTypes"].split(sep=SEP)
        service_types_objs = []
        for service_type_str in service_types_strs:
            service_type_obj, _ = KCentreServiceTypeModel.objects.get_or_create(service_type=service_type_str)
            service_types_objs.append(service_type_obj)

        resource_families_strs = row["ResFamilies"].split(sep=SEP)
        resource_families_objs = []
        for resource_family_str in resource_families_strs:
            resource_family_obj, _ = ResourceFamilyModel.objects.get_or_create(resource_family=resource_family_str)
            resource_families_objs.append(resource_family_obj)

        status_str = row["Status"].split(sep=SEP)
        status, _ = KCentreStatusModel.objects.get_or_create(status=status_str)

        centre_id = row["CentReg"]
        try:
            centre_id = int(centre_id)
            centre = CentreModel.objects.get(pk=centre_id)
        except Exception:
            centre = None

        kcentre = KCentreModel(
            audiences=row['Audiences'].split(sep=SEP),
            competence=row['CompetenceArea'],
            data_types=row['DataTypes'].split(sep=SEP),
            generic_topics=row['GenericTopics'].split(sep=SEP),
            keywords=row['KeyWords'].split(sep=SEP),
            language_processing_spec=row['LangProcessing'].split(sep=SEP),
            linguistic_topics=row['LingTopics'].split(sep=SEP),
            pid=row['PID'],
            tour_de_clarin_interview=row['TdCIntro'],
            tour_de_clarin_intro=row['TdCInterview'],
            website_language=row['PortalLang'].split(sep=SEP),
            centre_fk=centre,
            status_fk=status,
        )
        kcentre.save()
        kcentre.service_type_fk.set(service_types_objs)
        kcentre.resource_families_fks.set(resource_families_objs)
        kcentre.save()


class Migration(migrations.Migration):

    dependencies = [
        ('centre_registry', '0035_kcentre_models'),
    ]

    operations = [
        migrations.RunPython(forwards)
    ]

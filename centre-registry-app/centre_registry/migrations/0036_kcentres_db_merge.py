from django.conf import settings
from django.db import migrations, models
import logging
import pandas

logger = logging.getLogger(__name__)


def forwards(apps, schema_editor):
    logger.setLevel(logging.INFO)
    settings.LOGGING['loggers']['django'] = {
        'level': 'INFO',
        'handlers': ['console']
    }
    logger.critical("DEBUG Test")

    CentreModel = apps.get_model("centre_registry", "Centre")
    KCentreModel = apps.get_model("centre_registry", "KCentre")
    KCentreServiceTypeModel = apps.get_model("centre_registry", "KCentreServiceType")
    KCentreStatusModel = apps.get_model("centre_registry", "KCentreStatus")
    ResourceFamilyModel = apps.get_model("centre_registry", "ResourceFamily")
    SEP = ';'

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

        centre = None
        centre_id = row["CentReg"]
        try:
            centre_id = int(centre_id)
        except ValueError:
            centre_id = None
        logger.critical(f"DEBUG Centre ID {centre_id}")
        # REMOVE TRY CATCH FOR PRODUCTION MIGRATION, NO FIXTURES GENERATED FOR NEW MODELS YET
        try:
            if centre_id is not None:
                centre = CentreModel.objects.get(pk=centre_id)
            else:
                centre = None
        except Exception as e:
            centre = None

        # prepare values, santitise empty strings
        audiences = row['Audiences'].replace('\n', '').split(sep=SEP)
        competence = row['CompetenceArea']
        data_types = row['DataTypes'].replace('\n', '').split(sep=SEP)
        generic_topics = row['GenericTopics'].replace('\n', '').split(sep=SEP)
        keywords = row['KeyWords'].replace('\n', '').split(sep=SEP)
        languages_processed = row['Languages'].replace('\n', '').split(sep=SEP)
        language_processing_spec = row['LangProcessing'].replace('\n', '').split(sep=SEP)
        lingustic_topics = row['LingTopics'].replace('\n', '').split(sep=SEP)
        modalities = row['Modalities'].replace('\n', '').split(sep=SEP)
        pid = row['PID']
        tour_de_clarin_interview = row['TdCIntro']
        tour_de_clarin_intro = row['TdCInterview']
        website_language = row['PortalLang'].replace('\n', '').split(sep=SEP)

        kcentre = KCentreModel(
            audiences=audiences,
            competence=competence,
            data_types=data_types,
            generic_topics=generic_topics,
            keywords=keywords,
            languages_processed=languages_processed,
            language_processing_spec=language_processing_spec,
            linguistic_topics=lingustic_topics,
            modalities=modalities,
            pid=pid,
            tour_de_clarin_interview=tour_de_clarin_interview,
            tour_de_clarin_intro=tour_de_clarin_intro,
            website_language=website_language,
            centre_fk=centre,
            status_fk=status,
        )
        kcentre.save()
        kcentre.service_type_fks.set(service_types_objs)
        kcentre.resource_families_fks.set(resource_families_objs)
        kcentre.save()


class Migration(migrations.Migration):

    dependencies = [
        ('centre_registry', '0035_populate_organisation'),
    ]

    operations = [
        migrations.RunPython(forwards)
    ]

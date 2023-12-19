from django.core.management.base import BaseCommand, CommandError


from centre_registry.utils import populate_shadow_tables


class Command(BaseCommand):
    help = ("Reinitialized Shadow tables with production data\n"
            "Shadow tables store edit candidates to KCentre data submitted by external user for moderation")

    def handle(self, *args, **options):
        try:
            populate_shadow_tables()
        except Exception as err:
            raise CommandError(err)

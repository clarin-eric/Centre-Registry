from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = ("Reinitialized Shadow tables with production data\n"
            "Shadow tables store edit candidates to KCentre data submitted by external user for moderation")

    def handle(self, *args, **options):
        try:
            pass
        except Exception as e:
            raise CommandError("Error while attempting to populate shadow tables")

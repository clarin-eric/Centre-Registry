from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError
from django.test.client import RequestFactory

from centre_registry.models import


class Command(BaseCommand):
    help = 'Command to update certification status based on expiration date'

    def handle(self, *args, **options):



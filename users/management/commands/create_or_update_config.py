from django.core.management.base import BaseCommand

from accounts.models import CometServerConfiguration


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('url', type=str)
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)

    def handle(self, *args, **options):
        CometServerConfiguration.objects.all().delete()
        CometServerConfiguration.objects.create(
            url=options['url'],
            username=options['username'],
            password=options['password']
        )

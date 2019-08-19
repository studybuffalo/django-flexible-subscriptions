"""Django management command to process subscriptions via task runner."""
import importlib

from django.core.management.base import BaseCommand

from subscriptions.conf import SETTINGS


class Command(BaseCommand):
    """Django management command to process subscriptions via task runner."""
    help = 'Processes all subscriptions to handle renewal and expiries.'

    def handle(self, *args, **options):
        """Runs Manager methods required to process subscriptions."""
        Manager = getattr( # pylint: disable=invalid-name
            importlib.import_module(SETTINGS['management_manager']['module']),
            SETTINGS['management_manager']['class']
        )
        manager = Manager()

        self.stdout.write('Processing subscriptions... ', ending='')
        manager.process_subscriptions()
        self.stdout.write('Complete!')

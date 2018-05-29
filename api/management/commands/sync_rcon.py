from django.core.management.base import BaseCommand
from api.tasks import sync_server_rcon_task

class Command(BaseCommand):
    help = 'Sync RCON for a specific server'

    def add_arguments(self, parser):
        parser.add_argument('server_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for server_id in options['server_id']:
            sync_server_rcon_task(server_id)

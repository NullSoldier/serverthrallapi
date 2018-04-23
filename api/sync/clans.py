from django.db import transaction
from django.db.models import Q

from api.models import Clan, Server


def sync_clans(server_id, data):
    server = (Server.objects
        .filter(id=server_id)
        .first())

    if server is None:
        return

    with transaction.atomic():
        # Delete removed clans
        sent_ids = [c['id'] for c in data]

        (Clan.objects
            .filter(server=server)
            .filter(~Q(conan_id__in=sent_ids))
            .delete())

        for sync_data in data:
            clan = (Clan.objects
                .filter(conan_id=sync_data['id'])
                .first())

            if clan is None:
                clan = Clan()

            clan.server = server
            clan.conan_id = sync_data['id']
            clan.name = sync_data['name']
            clan.motd = sync_data['motd']
            clan.owner_id = sync_data['owner_id']
            clan.save()

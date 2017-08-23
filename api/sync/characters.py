from datetime import datetime

import pytz
from django.db import transaction
from django.db.models import Q

from api.models import Character, CharacterHistory, Server


def _sync_character(server, character, data):
    has_no_changes = (
        (data['x'] == character.x) or
        (data['y'] == character.y) or
        (data['z'] == character.y))

    last_online = (datetime
        .utcfromtimestamp(data['last_online'])
        .replace(tzinfo=pytz.utc))

    character.server         = server
    character.conan_id       = data['conan_id']
    character.name           = data['name']
    character.level          = data['level']
    character.is_online      = data['is_online']
    character.steam_id       = data['steam_id']
    character.last_killed_by = data['last_killed_by']
    character.x              = data['x']
    character.y              = data['y']
    character.z              = data['z']
    character.last_online    = last_online
    character.save()

    return not has_no_changes


def sync_characters(server_id, data, params):
    server = (Server.objects
        .filter(id=server_id)
        .first())

    if server is None:
        return

    with transaction.atomic():
        history_buffer = []
        changed_ids = []

        # Delete removed characters
        sent_ids = [c['conan_id'] for c in data]
        (Character.objects
            .filter(server=server)
            .filter(~Q(conan_id__in=sent_ids))
            .delete())

        for sync_data in data:
            character = (Character.objects
                .filter(server=server)
                .filter(conan_id=sync_data['conan_id'])
                .first())

            if character is None:
                character = Character()

            changed = _sync_character(server, character, data)

            if changed:
                changed_ids.append(character.id)
                history_buffer.append(character.generate_history())

        has_ginfo = (
            'ginfo_group_uid' in params and
            'ginfo_access_token' in params)

        if has_ginfo:
            from api.tasks import sync_ginfo_task
            sync_ginfo_task.delay(changed_ids,
                params['ginfo_group_uid'],
                params['ginfo_access_token'])

        CharacterHistory.objects.bulk_create(history_buffer)

from api.models import Clan, Character, CharacterHistory, ServerSyncData
from datetime import datetime
from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
import json
import pytz


def sync_characters(server, data):
    now = timezone.now()
    history_buffer = []
    changed_ids = []

    # Delete removed characters
    sent_ids = [c['conan_id'] for c in data]
    (Character.objects
        .filter(server=server)
        .filter(~Q(conan_id__in=sent_ids))
        .delete())

    character_map = {}

    for sync_data in data:
        character = (Character.objects
            .filter(server=server)
            .filter(conan_id=sync_data['conan_id'])
            .first())

        if character is None:
            character = Character()

        has_moved = (
            (data['x'] == character.x) or
            (data['y'] == character.y) or
            (data['z'] == character.y))

        last_online = (datetime
            .utcfromtimestamp(data['last_online'])
            .replace(tzinfo=pytz.utc))

        character.server         = server
        character.clan_id        = None
        character.conan_id       = data['conan_id']
        character.conan_clan_id  = data['clan_id']
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

        character_map[character.conan_id] = character

        if has_moved:
            changed_ids.append(character.id)
            history_buffer.append(character.generate_history(now))

    if settings.ST_ENABLE_HISTORY:
        CharacterHistory.objects.bulk_create(history_buffer)

    return character_map, changed_ids


def sync_clans(server, data):
    # Delete clans we werent sent
    sent_ids = [c['id'] for c in data]
    (Clan.objects
        .filter(server=server)
        .filter(~Q(conan_id__in=sent_ids))
        .delete())

    clan_map = {}

    for sync_data in data:
        clan = (Clan.objects
            .filter(
                server=server,
                conan_id=sync_data['id'])
            .first())

        if clan is None:
            clan = Clan()

        clan.server = server
        clan.owner_id = None
        clan.conan_id = sync_data['id']
        clan.conan_owner_id = sync_data['owner_id']
        clan.name = sync_data['name']
        clan.motd = sync_data['motd']
        clan.save()

        clan_map[clan.conan_id] = clan

    return clan_map


def fix_primary_keys(character_map, clan_map):
    for character in character_map.values():
        if character.conan_clan_id in clan_map:
            character.clan = clan_map[character.conan_clan_id]
            character.save()

    for clan in clan_map.values():
        if clan.conan_owner_id in character_map:
            clan.owner = character_map[clan.conan_owner_id]
            clan.save()


def sync_server_data(sync_data_id, request_get_params):
    sync_data = (ServerSyncData.objects
        .filter(id=sync_data_id)
        .select_related('server')
        .first())

    sync_data.delete()
    server = sync_data.server

    if sync_data is None:
        return

    if server.last_sync >= sync_data.created:
        return

    data = json.loads(sync_data.data)
    changed_character_ids = []

    with transaction.atomic():
        if 'server' in data:
            server.name = data['server'].get('name', '')
            server.ip_address = data['server'].get('ip_address', '')

        if 'characters' in data:
            character_map, changed_character_ids = sync_characters(server, data['characters'])

        if 'clans' in data:
            clan_map = sync_clans(server, data['clans'])

        fix_primary_keys(character_map, clan_map)

        server.last_sync = timezone.now()
        server.save()

    has_ginfo = (
        'ginfo_group_uid' in request_get_params and
        'ginfo_access_token' in request_get_params)

    if has_ginfo:
        from api.tasks import sync_ginfo_task
        sync_ginfo_task.delay(changed_character_ids,
            request_get_params['ginfo_group_uid'],
            request_get_params['ginfo_access_token'])

    from api.tasks import delete_old_history_task
    delete_old_history_task.delay()

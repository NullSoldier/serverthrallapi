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
            (sync_data['x'] == character.x) or
            (sync_data['y'] == character.y) or
            (sync_data['z'] == character.y))

        last_online = (datetime
            .utcfromtimestamp(sync_data['last_online'])
            .replace(tzinfo=pytz.utc))

        character.server         = server
        character.clan_id        = None
        character.conan_id       = sync_data['conan_id']
        character.conan_clan_id  = sync_data.get('clan_id')
        character.name           = sync_data['name']
        character.level          = sync_data['level']
        character.is_online      = sync_data['is_online']
        character.steam_id       = sync_data['steam_id']
        character.last_killed_by = sync_data['last_killed_by']
        character.x              = sync_data['x']
        character.y              = sync_data['y']
        character.z              = sync_data['z']
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


def get_int(data, key, default=None):
    if key not in data:
        return default
    try:
        return int(data[key])
    except ValueError:
        return default


def remove_outer_quotes(value):
    if value.startswith('"'):
        value = value[1:]
    if value.endswith('"'):
        value = value[:len(value) - 1]
    return value


def sync_server_data(sync_data_id, request_get_params):
    sync_data = (ServerSyncData.objects
        .filter(id=sync_data_id)
        .select_related('server')
        .first())

    if sync_data is None:
        print 'Dropping sync request because data is invalid'
        return

    sync_data.delete()
    server = sync_data.server

    if server.last_sync and server.last_sync >= sync_data.created:
        print "Dropping stale sync request"
        return

    data = json.loads(sync_data.data)
    changed_character_ids = []

    with transaction.atomic():
        if 'version' in data:
            server.version = data['version']

        if 'server' in data:
            server.name = remove_outer_quotes(data['server'].get('name', ''))
            server.ip_address = data['server'].get('ip_address', '')
            server.query_port = get_int(data['server'], 'query_port')
            server.max_players = get_int(data['server'], 'max_players')
            server.tick_rate = get_int(data['server'], 'tick_rate')

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

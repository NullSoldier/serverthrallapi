from api.models import Server, ServerSyncData
from valve.rcon import RCON, RCONError
import json

def from_int_bool(v):
    return bool(int(v))

def execute_rcon(rcon_host, rcon_port, rcon_password, command):
    print('Executing on %s:%s %s' % (rcon_host, rcon_port, command))

    try:
        with RCON((rcon_host, rcon_port), rcon_password) as rcon:
            return rcon.execute(command)
    except RCONError:
        print('Error sending command ' + command)
    except Exception as ex:
        print('Error when exceuting RCON command')
        raise ex

def execute_rcon_sql(server, sql, type_map):
    response = execute_rcon(
        rcon_host=server.rcon_host,
        rcon_port=server.rcon_port,
        rcon_password=server.rcon_password,
        command='sql %s' % sql)

    if response is None:
        return False, []

    return True, parse_response_into_rows(response, type_map)

def parse_response_into_rows(response, type_map):
    print "RESPNOSE", response.text
    print 'TYPE-MAP', type_map

    rows = []

    for row_index, line in enumerate(response.text.splitlines()):

        if row_index == 0:
            continue

        print "ROW", row_index, line

        row = []
        for col_index, col in enumerate(line.split('|')):

            if col_index == 0:
                col = col.replace('#%s' % (row_index - 1), '')

            type_transform = type_map[col_index]
            row.append(type_transform(col.strip()))

        rows.append(row)

    return rows

def get_characters(server):
    is_success, rows = execute_rcon_sql(server, '''
        SELECT
            acc.online,
            ch.id,
            ch.char_name,
            ch.level,
            ch.playerId,
            ch.lastTimeOnline,
            ch.killerName,
            ch.guild,
            act.x,
            act.y,
            act.z
        FROM characters AS ch
        LEFT JOIN account AS acc ON ch.playerId = acc.user
        LEFT JOIN actor_position AS act ON ch.id = act.id;
    ''', [from_int_bool, int, unicode, int, unicode, int, unicode, int, float, float, float])

    if not is_success:
        return None

    characters = []

    for row in rows:
        characters.append({
            'name': row[2],
            'level': row[3],
            'is_online': row[0],
            'steam_id': row[4],
            'conan_id': row[1],
            'last_killed_by': row[6],
            'last_online': row[5],
            'clan_id': row[7],
            'x': row[8],
            'y': row[9],
            'z': row[10]})

    return characters

def get_clans(server):
    is_success, rows = execute_rcon_sql(server, '''
        SELECT guildId, name, owner, messageOfTheDay FROM guilds
    ''', [int, unicode, int, unicode])

    if not is_success:
        return None

    guilds = []

    for row in rows:
        guilds.append({
            'id': row[0],
            'name': row[1],
            'owner_id': row[2],
            'motd': row[3]
        })

    return guilds

def sync_server_rcon(server_id):
    server = (Server.objects
        .filter(id=server_id)
        .first())

    is_valid = (
        server is not None and
        server.rcon_host is not None and
        server.rcon_password is not None and
        server.rcon_port is not None)

    if not is_valid:
        return

    characters = get_characters(server)
    clans = get_clans(server)

    # if clans is not None:
    #     for character in characters:
    #         print character

    # if clans is not None:
    #     for clan in clans:
    #         print clan

    is_valid_sync = (
        clans is not None and
        characters is not None)

    if not is_valid_sync:
        return

    sync_data = ServerSyncData.objects.create(server=server, data=json.dumps({
        'version': 'api',
        'characters': characters,
        'clans': clans
    }))

    from api.tasks import sync_server_data_task
    sync_server_data_task(sync_data.id, {})

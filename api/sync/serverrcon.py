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

def execute_rcon_sql(server, build_sql, paginate_predicate, col_type_map):
    last_col_paginate = -1
    results = []

    while True:
        response = execute_rcon(
            rcon_host=server.rcon_host,
            rcon_port=server.rcon_port,
            rcon_password=server.rcon_password,
            command='sql %s' % build_sql(last_col_paginate))

        if response is None:
            return False, []

        rows = parse_response_into_rows(response, col_type_map)

        if len(rows) == 0:
            break

        last_col_paginate = paginate_predicate(rows[len(rows) - 1])
        results = results + rows

    return True, results

def parse_response_into_rows(response, col_type_map):
    rows = []

    for row_index, line in enumerate(response.body.splitlines()):

        print line

        if row_index == 0:
            continue

        # print "ROW `%s`" % (line)

        row = []
        for col_index, col in enumerate(line.split('|')):
            col = col.strip()

            if col_index >= len(col_type_map):
                continue

            if col_index == 0:
                col = col.replace('#%s' % (row_index - 1), '').strip()

            if col == 'void':
                col = None

            if col is not None:
                type_transform = col_type_map[col_index]
                col = type_transform(col)

            row.append(col)

        rows.append(row)

    return rows

def get_characters(server):
    def build_sql(paginate_value):
        return '''
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
            LEFT JOIN actor_position AS act ON ch.id = act.id
            WHERE ch.id > %s
            ORDER BY ch.id
            LIMIT 20
        ''' % paginate_value

    def paginate_predicate(r):
        return r[1]

    is_success, rows = execute_rcon_sql(server, build_sql, paginate_predicate,
        [from_int_bool, int, str, int, str, int, str, int, float, float, float])

    if not is_success:
        return None

    characters = []

    for row in rows:
        characters.append({
            'is_online': row[0],
            'conan_id': row[1],
            'name': row[2],
            'level': row[3],
            'steam_id': row[4],
            'last_online': row[5],
            'last_killed_by': row[6],
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
        server.sync_rcon and
        server is not None and
        server.rcon_host is not None and
        server.rcon_password is not None and
        server.rcon_port is not None)

    if not is_valid:
        return

    characters = get_characters(server)
    # clans = get_clans(server)

    # if clans is not None:
    #     for character in characters:
    #         print character

    # if clans is not None:
    #     for clan in clans:
    #         print clan

    return

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

from .sync import sync_server_data, sync_ginfo, sync_server_rcon
from api.models import Server
from serverthrallapi.celery import app


@app.task()
def sync_ginfo_task(character_ids, group_uid, access_token):
    sync_ginfo(character_ids, group_uid, access_token)


@app.task()
def sync_server_data_task(sync_data_id, request_get_params):
    sync_server_data(sync_data_id, request_get_params)


@app.task()
def sync_server_rcon_task(server_id):
    sync_server_rcon(server_id)


@app.task()
def sync_all_rcon_servers_task():
    server_ids = (Server.objects
        .filter(rcon_host__isnull=False)
        .values_list('id', flat=True))

    for server_id in server_ids:
        sync_server_rcon_task(server_id)

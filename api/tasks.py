from .sync import sync_ginfo, sync_characters, sync_clans
from api.models import CharacterHistory
from datetime import timedelta
from django.utils import timezone
from serverthrallapi.celery import app


@app.task()
def sync_clans_task(server_id, clan_data):
    sync_clans(server_id, clan_data)


@app.task()
def sync_characters_task(server_id, character_data, params):
    sync_characters(server_id, character_data, params)


@app.task()
def sync_ginfo_task(character_ids, group_uid, access_token):
    sync_ginfo(character_ids, group_uid, access_token)


@app.task()
def delete_old_history():
    history_threshold = timezone.now() - timedelta(days=5)
    CharacterHistory.objects.filter(created__lt=history_threshold).delete()

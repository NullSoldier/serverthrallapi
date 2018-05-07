from .sync import sync_server_data, sync_ginfo
from api.models import CharacterHistory
from datetime import timedelta
from django.utils import timezone
from serverthrallapi.celery import app


@app.task()
def sync_ginfo_task(character_ids, group_uid, access_token):
    sync_ginfo(character_ids, group_uid, access_token)


@app.task()
def sync_server_data_task(sync_data_id, request_get_params):
    sync_server_data(sync_data_id, request_get_params)


@app.task()
def delete_old_history_task():
    history_threshold = timezone.now() - timedelta(days=5)
    CharacterHistory.objects.filter(created__lt=history_threshold).delete()

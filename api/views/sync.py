import json

from django.http import HttpResponse
from django.utils import timezone

from api.models import Server
from api.tasks import delete_old_history, sync_characters_task, sync_clans_task

from .base import BaseAdminView


class SyncCharactersView(BaseAdminView):

    def post(self, request, server_id):
        if 'private_secret' not in request.GET:
            return HttpResponse('missing required param private_secret', status=400)

        server = (Server.objects
            .filter(id=server_id, private_secret=request.GET['private_secret'])
            .first())

        if server is None:
            return HttpResponse('server does not exist', status=404)

        data = json.loads(request.body)

        if 'characters' in data:
            sync_characters_task.delay(server.id, data['characters'], request.GET)

        if 'clans' in data:
            sync_clans_task.delay(server.id, data['clans'])

        server.last_sync = timezone.now()
        server.save()

        delete_old_history.delay()
        return HttpResponse(status=200)

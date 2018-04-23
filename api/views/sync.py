import json

from django.http import HttpResponse
from django.utils import timezone

from api.tasks import delete_old_history, sync_characters_task, sync_clans_task

from .base import BaseView


class SyncCharactersView(BaseView):

    def post(self, request, server_id):
        if 'private_secret' not in request.GET:
            return HttpResponse('missing required param private_secret', status=400)

        server = self.get_server_private(request, server_id)

        if server is None:
            return HttpResponse('server does not exist', status=404)

        data = json.loads(request.body)

        if 'server' in data:
            server.name = data['server']['name']

        if 'characters' in data:
            sync_characters_task.delay(server.id, data['characters'], request.GET)

        if 'clans' in data:
            sync_clans_task.delay(server.id, data['clans'])

        server.last_sync = timezone.now()
        server.save()

        delete_old_history.delay()
        return HttpResponse(status=200)

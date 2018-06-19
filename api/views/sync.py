from django.http import HttpResponse

from api.tasks import sync_server_data_task
from api.models import ServerSyncData

from .base import BaseView


class SyncCharactersView(BaseView):

    def post(self, request, server_id):
        if 'private_secret' not in request.GET:
            return HttpResponse('missing required param private_secret', status=400)

        server = self.get_server_private(request, server_id)

        if server is None:
            return HttpResponse('server does not exist', status=404)

        sync_data = ServerSyncData.objects.create(
            server=server,
            data=request.body)

        sync_server_data_task.delay(sync_data.id, request.GET)
        return HttpResponse(status=200)

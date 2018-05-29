from django.http import HttpResponse, JsonResponse

from api.serializers import ServerSerializer, ServerAdminSerializer

from .base import BaseView
import json


class ServerView(BaseView):

    def get(self, request, server_id):
        server = self.get_server_public(request, server_id)

        if server is None:
            return HttpResponse('server does not exist', status=404)

        serialized = ServerSerializer(server).data
        return JsonResponse(serialized, status=200)

    def post(self, request, server_id):
        if 'private_secret' not in request.GET:
            return HttpResponse('missing required param private_secret')

        server = self.get_server_private(request, server_id)

        if server is None:
            return HttpResponse('server does not exist', status=404)

        data = json.loads(request.body)

        if 'sync_rcon' in data:
            server.sync_rcon = data['sync_rcon']
        if 'rcon_host' in data:
            server.rcon_host = data['rcon_host']
            server.ip_address = data['rcon_host']
        if 'rcon_port' in data:
            server.rcon_port = data['rcon_port']
        if 'rcon_password' in data:
            server.rcon_password = data['rcon_password']

        # TODO: If sync_rcon is true, and credentials are different
        # check RCON credentials work before creating or editing the server

        server.save()
        server.refresh_from_db()

        serialized = ServerAdminSerializer(server).data
        return JsonResponse(serialized, status=200)

from uuid import uuid1

from django.http import JsonResponse

from api.models import Server
from api.serializers import ServerAdminSerializer, ServerSerializer

from .base import BaseView
import json


class ServersView(BaseView):

    def get(self, request):
        servers = self.get_servers().only_active()
        serialized = ServerSerializer(servers, many=True).data
        return JsonResponse({'items': serialized})

    def post(self, request):
        server = Server()
        server.private_secret = uuid1()

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

        server.save()

        server = self.get_server_public(request, server.id)
        serialized = ServerAdminSerializer(server).data
        return JsonResponse(serialized, status=200)

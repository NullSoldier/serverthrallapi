from uuid import uuid1

from django.http import JsonResponse

from api.models import Server
from api.serializers import ServerAdminSerializer, ServerSerializer

from .base import BaseView


class ServersView(BaseView):

    def get(self, request):
        servers = self.get_servers()
        serialized = ServerSerializer(servers, many=True).data
        return JsonResponse({'items': serialized})

    def post(self, request):
        server = Server()
        server.private_secret = uuid1()
        server.save()

        server = self.get_server_public(request, server.id)
        serialized = ServerAdminSerializer(server).data
        return JsonResponse(serialized, status=200)

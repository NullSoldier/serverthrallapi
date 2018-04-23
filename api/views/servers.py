from uuid import uuid1

from django.http import JsonResponse

from api.models import Server
from api.serializers import ServerAdminSerializer, ServerSerializer

from .base import BaseView


class ServersView(BaseView):

    def post(self, request):
        server = Server()
        server.private_secret = uuid1()
        server.save()

        serialized = ServerAdminSerializer(server).data
        return JsonResponse(serialized, status=200)

    def get(self, request):
        servers = Server.objects.only_active().with_character_count()
        serialized = ServerSerializer(servers, many=True).data
        return JsonResponse({'items': serialized})

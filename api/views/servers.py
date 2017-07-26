from uuid import uuid1

from django.http import JsonResponse

from api.models import Server
from api.serializers import ServerAdminSerializer

from .base import BasePublicView


class ServersView(BasePublicView):

    def post(self, request):
        server = Server()
        server.private_secret = uuid1()
        server.save()

        serialized = ServerAdminSerializer(server).data
        return JsonResponse(serialized, status=200)

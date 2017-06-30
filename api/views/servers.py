from .base import BasePublicView
from api.models import Server
from api.serializers import ServerAdminSerializer
from django.http import JsonResponse
from uuid import uuid1


class ServersView(BasePublicView):

	def post(self, request):
		server = Server()
		server.private_secret = uuid1()
		server.save()

		serialized = ServerAdminSerializer(server).data
		return JsonResponse(serialized, status=200)
from .base import BasePublicView
from api.models import Character, Server
from api.serializers import CharacterSerializer
from django.db.models import Q
from django.http import JsonResponse, HttpResponse


class CharactersView(BasePublicView):

	def get(self, request, server_id):
		server = self.get_server(request, server_id)

		if server is None:
			return HttpResponse('server does not exist', status=400)

		characters = (Character.objects
			.filter(server_id=server.id)
			.all())

		serialized = CharacterSerializer(characters, many=True).data
		return JsonResponse(serialized, status=200, safe=False)
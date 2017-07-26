from django.http import HttpResponse, JsonResponse

from api.models import Character
from api.serializers import CharacterSerializer

from .base import BasePublicView


class CharacterView(BasePublicView):

    def get(self, request, server_id, character_id):
        server = self.get_server(request, server_id)

        if server is None:
            return HttpResponse('server does not exist', status=400)

        character = (Character.objects
            .filter(
                server_id=server.id,
                id=character_id)
            .first())

        if character is None:
            return HttpResponse('character does not exist', status=400)

        serialized = CharacterSerializer(character).data
        return JsonResponse(serialized, status=200)

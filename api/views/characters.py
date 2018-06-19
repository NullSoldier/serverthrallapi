from django.http import HttpResponse, JsonResponse

from api.models import Character
from api.serializers import CharacterSerializer

from .base import BaseView


class CharactersView(BaseView):

    def get(self, request, server_id):
        server = self.get_server_public(request, server_id)

        if server is None:
            return HttpResponse('server does not exist', status=400)

        characters = (Character.objects
            .filter(server_id=server.id)
            .select_related('clan')
            .all())

        serialized = CharacterSerializer(characters, many=True).data
        return JsonResponse(serialized, status=200, safe=False)

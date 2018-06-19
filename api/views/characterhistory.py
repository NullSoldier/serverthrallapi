from django.http import HttpResponse, JsonResponse

from api.models import Character, CharacterHistory
from api.serializers import CharacterHistorySerializer

from .base import BaseView


class CharacterHistoryView(BaseView):

    def get(self, request, server_id, character_id):
        server = self.get_server_public(request, server_id)

        if server is None:
            return HttpResponse('server does not exist', status=400)

        character = (Character.objects
            .filter(
                server_id=server.id,
                id=character_id)
            .first())

        if character is None:
            return HttpResponse('character does not exist', status=400)

        histories = CharacterHistory.objects.filter(character_id=character.id)
        serialized = CharacterHistorySerializer(histories, many=True).data
        return JsonResponse({'history': serialized}, status=200)

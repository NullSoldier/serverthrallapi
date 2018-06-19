from django.http import HttpResponse, JsonResponse

from api.models import Character, Clan
from api.serializers import CharacterSerializer

from .base import BaseView


class ClanCharactersView(BaseView):

    def get(self, request, server_id, clan_id):
        server = self.get_server_public(request, server_id)

        if server is None:
            return HttpResponse('server does not exist', status=400)

        clan = Clan.objects.filter(server_id=server.id, id=clan_id).first()

        if clan is None:
            return HttpResponse('clan does not exist', status=400)

        characters = (Character.objects
            .filter(server_id=server.id, clan_id=clan_id)
            .select_related('clan')
            .all())

        serialized = CharacterSerializer(characters, many=True).data
        return JsonResponse(serialized, status=200, safe=False)

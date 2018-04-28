from django.http import HttpResponse, JsonResponse

from api.models import Clan
from api.serializers import ClanSerializer

from .base import BaseView


class ClanView(BaseView):

    def get(self, request, server_id, clan_id):
        server = self.get_server_public(request, server_id)

        if server is None:
            return HttpResponse('server does not exist', status=400)

        clan = (Clan.objects
            .filter(
                server_id=server.id,
                id=clan_id)
            .with_owner_name()
            .with_character_count()
            .first())

        if clan is None:
            return HttpResponse('clan does not exist', status=400)

        serialized = ClanSerializer(clan).data
        return JsonResponse(serialized, status=200)

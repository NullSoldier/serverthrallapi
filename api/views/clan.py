from .base import BasePublicView
from api.serializers import ClanSerializer
from django.http import JsonResponse, HttpResponse


class ClanView(BasePublicView):

    def get(self, request, _id, clan_id):
        server = self.get_server(request, server_id)

        if server is None:
            return HttpResponse('server does not exist', status=400)

        clan = (Clan.objects
            .filter(
                server_id=server.id,
                id = clan_id)
            .first())

        if clan is None:
            return HttpResponse('clan does not exist', status=400)

        serialized = ClanSerializer(clan).data
        return JsonResponse(serialized, status=200)

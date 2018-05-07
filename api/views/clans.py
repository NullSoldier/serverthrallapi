from django.http import HttpResponse, JsonResponse

from api.models import Clan
from api.serializers import ClanSerializer

from .base import BaseView


class ClansView(BaseView):

    def get(self, request, server_id):
        server = self.get_server_public(request, server_id)

        if server is None:
            return HttpResponse('server does not exist', status=400)

        clans = (Clan.objects
            .filter(server_id=server.id)
            .select_related('owner')
            .with_character_count()
            .all())

        serialized = ClanSerializer(clans, many=True).data
        return JsonResponse(serialized, status=200, safe=False)

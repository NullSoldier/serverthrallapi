from django.http import HttpResponse, JsonResponse

from api.models import Clan
from api.serializers import ClanSerializer

from .base import BasePublicView


class ClansView(BasePublicView):

    def get(self, request, server_id):
        server = self.get_server(request, server_id)

        if server is None:
            return HttpResponse('server does not exist', status=400)

        clans = (Clan.objects
            .filter(server_id=server.id)
            .all())

        serialized = ClanSerializer(clans, many=True).data
        return JsonResponse(serialized, status=200, safe=False)

from .base import BasePublicView
from api.models import Clan, Server
from api.serializers import ClanSerializer
from django.db.models import Q
from django.http import JsonResponse, HttpResponse


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

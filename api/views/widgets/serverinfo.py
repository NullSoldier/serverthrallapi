from django.http import JsonResponse

from api.models import Server, Character, Clan

from ..base import BaseView


class ServerInfoView(BaseView):

    def get(self, request):
        data = {
            'server_count': Server.objects.count(),
            'character_count': Character.objects.count(),
            'clan_count': Clan.objects.count()
        }
        return JsonResponse(data, status=200, safe=False)

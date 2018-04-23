from django.http import HttpResponse, JsonResponse

from api.serializers import ServerSerializer, ServerAdminSerializer

from .base import BaseView


class ServerView(BaseView):

    def get(self, request, server_id):
        server = self.get_server_public(request, server_id)

        if server is None:
            return HttpResponse('server does not exist', status=404)

        serialized = ServerSerializer(server).data
        return JsonResponse(serialized, status=200)

    def post(self, request, server_id):
        if 'private_secret' not in request.GET:
            return HttpResponse('missing required param private_secret')

        data = request.GET
        server = self.get_server_private(request, server_id)

        if server is None:
            return HttpResponse('server does not exist', status=404)

        if 'name' in data:
            server.name = data['name']

        server.save()

        serialized = ServerAdminSerializer(server).data
        return JsonResponse(serialized, status=200)

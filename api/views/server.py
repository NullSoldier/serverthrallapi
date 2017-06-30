from .base import BaseAdminView
from api.models import Server
from api.serializers import ServerAdminSerializer
from django.http import JsonResponse, HttpResponse


class ServerView(BaseAdminView):
	def get(self, request, server_id):
		if 'private_secret' not in request.GET:
			return HttpResponse('missing required param private_secret')

		data = request.GET

		server = self.get_server(request, server_id)

		if server is None:
			return HttpResponse('server does not exist', status=404)

		serialized = ServerAdminSerializer(server).data
		return JsonResponse(serialized, status=200)

	def post(self, request):
		if 'private_secret' not in request.GET:
			return HttpResponse('missing required param private_secret')

		data = request.GET
		server = self.get_server(request, server_id)

		if server is None:
			return HttpResponse('server does not exist', status=404)

		if 'name' in data:
			server.name = data['name']

		server.save()

		serialized = ServerAdminSerializer(server).data
		return JsonResponse(data, status=200)
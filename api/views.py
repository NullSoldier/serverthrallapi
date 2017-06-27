from __future__ import unicode_literals
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse
from api.models import Character, Server
from django.db.models import Q
from api.serializers import CharacterSerializer, ServerAdminSerializer
from uuid import uuid1
from uuid import UUID
from django.db import transaction
from datetime import datetime
import json
import pytz


class BasePublicView(View):

	def get_server(request, server_id):
		return (Server.objects
			.filter(id=server_id)
			.filter(
				Q(private_secret=request.GET.get('private_secret', None)) |
				Q(public_secret=request.GET.get('public_secret', None)))
			.first())


class BaseAdminView(View):

	def get_server(request, server_id):
		return = (Server.objects
			.filter(id=server_id)
			.filter(public_secret=request.GET.get('public_secret', None))
			.first())


class CharactersView(BasePublicView):

	def get(self, request, server_id):
		server = (Server.objects
			.filter(id=server_id)
			.filter(
				Q(private_secret=request.GET.get('private_secret', None)) |
				Q(public_secret=request.GET.get('public_secret', None)))
			.first())

		if server is None:
			return HttpResponse('server does not exist', status=400)

		characters = (Character.objects
			.filter(server_id=server.id)
			.all())

		serialized = CharacterSerializer(characters, many=True).data
		return JsonResponse(serialized, status=200, safe=False)


class CharacterView(BasePublicView):

	def get(self, request, server_id, character_id):
		server = (Server.objects
			.filter(id=server_id)
			.first())

		if server is None:
			return HttpResponse('server does not exist', status=400)

		character = (Character.objects
			.filter(
				server_id=server.id,
				id = character_id)
			.first())

		if character is None:
			return HttpResponse('character does not exist', status=400)

		serialized = CharacterSerializer(character).data
		return JsonResponse(serialized, status=200)


class ServersViews(BasePublicView):

	def post(self, request):
		server = Server()
		server.public_secret = uuid1()
		server.private_secret = uuid1()
		server.save()

		serialized = ServerAdminSerializer(server).data
		return JsonResponse(serialized, status=200)


class ServerView(BaseAdminView):
	def get(self, request, server_id):
		if 'private_secret' not in request.GET:
			return HttpResponse('missing required param private_secret')

		data = request.GET

		server = (Server.objects
			.filter(id=server_id, private_secret=data['private_secret'])
			.first())

		if server is None:
			return HttpResponse('server does not exist', status=404)

		serialized = ServerAdminSerializer(server).data
		return JsonResponse(serialized, status=200)

	def post(self, request):
		if 'private_secret' not in request.GET:
			return HttpResponse('missing required param private_secret')

		data = request.GET

		server = (Server.objects
			.filter(id=server_id, private_secret=data['private_secret'])
			.first())

		if server is None:
			return HttpResponse('server does not exist', status=404)

		server = Server()
		if 'name' in data:
			server.name = data['name']
		server.save()

		serialized = ServerAdminSerializer(server).data
		return JsonResponse(data, status=200)


class SyncCharactersView(BaseAdminView):

	def post(self, request, server_id):
		if 'private_secret' not in request.GET:
			return HttpResponse('missing required param private_secret', status=400)

		data = json.loads(request.body)

		if 'characters' not in data:
			return HttpResponse('missing required param characters', status=400)

		server = (Server.objects
			.filter(id=server_id, private_secret=request.GET['private_secret'])
			.first())

		if server is None:
			return HttpResponse('server does not exist', status=404)

		with transaction.atomic():
			# Delete removed characters
			id_set = [c['conan_id'] for c in data['characters']]
			Character.objects.filter(server=server).filter(~Q(conan_id__in=id_set)).delete()

			for sync_data in data['characters']:

				character = (Character.objects
					.filter(conan_id=sync_data['conan_id'])
					.first())

				if character is None:
					character = Character()

				last_online = (datetime
					.utcfromtimestamp(sync_data['last_online'])
					.replace(tzinfo=pytz.utc))

				character.conan_id = sync_data['conan_id']
				character.server = server
				character.name = sync_data['name']
				character.level = sync_data['level']
				character.is_online = sync_data['is_online']
				character.steam_id = sync_data['steam_id']
				character.last_killed_by = sync_data['last_killed_by']
				character.x = sync_data['x']
				character.y = sync_data['y']
				character.z = sync_data['z']
				character.last_online = last_online
				character.save()

		return HttpResponse(status=200)
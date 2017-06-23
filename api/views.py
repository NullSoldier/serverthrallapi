from __future__ import unicode_literals
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse
from api.models import Character, Server
from django.db.models import Q
from api.serializers import CharacterSerializer, ServerAdminSerializer
from uuid import uuid1
from django.db import transaction
from datetime import datetime
import json


class CharactersView(View):

	def get(self, request, server_id):
		server = (Server.objects
			.filter(id=server_id)
			.first())

		if server is None:
			return HttpResponse('server does not exist', status=400)

		characters = (Character.objects
			.filter(server_id=server.id)
			.all())

		serialized = CharacterSerializer(characters, many=True).data
		return JsonResponse(serialized, status=200, safe=False)


class CharacterView(View):

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


class ServersViews(View):

	def post(self, request):
		server = Server()
		server.public_secret = uuid1()
		server.private_secret = uuid1()
		server.save()

		serialized = ServerAdminSerializer(server).data
		return JsonResponse(data, status=200)


class ServerView(View):
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


class SyncCharactersView(View):

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
			Character.objects.filter(server=server).delete()

			for character in data['characters']:
				last_online = datetime.utcfromtimestamp(character['last_online'])

				Character.objects.create(
					server=server,
					name=character['name'],
					level=character['level'],
					is_online=character['is_online'],
					steam_id=character['steam_id'],
					conan_id=character['conan_id'],
					last_killed_by=character['last_killed_by'],
					last_online=last_online,
					x=character['x'],
					y=character['y'],
					z=character['z'])

		return HttpResponse(status=200)
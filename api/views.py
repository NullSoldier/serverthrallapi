# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse
from api.models import Character, Server
from django.db.models import Q
from api.serializers import CharacterSerializer


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

		data = CharacterSerializer(characters, many=True).data
		return JsonResponse(data, status=200, safe=False)

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

		data = CharacterSerializer(character).data
		return JsonResponse(data, status=200)
from django.conf.urls import url, include
from django.contrib import admin
from .views import CharactersView, CharacterView

urlpatterns = [
	url(r'^(?P<server_id>\d+)/characters$', CharactersView.as_view()),
	url(r'^(?P<server_id>\d+)/characters/(?P<character_id>\d+)$', CharacterView.as_view())
]

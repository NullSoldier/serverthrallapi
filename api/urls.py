from django.conf.urls import url, include
from django.contrib import admin
from .views import CharactersView, CharacterView, ServersViews, ServerView, SyncCharactersView

urlpatterns = [
	url(r'^$', ServersViews.as_view()),
	url(r'^(?P<server_id>\d+)$', ServerView.as_view()),
	url(r'^(?P<server_id>\d+)/sync/characters$', SyncCharactersView.as_view()),
	url(r'^(?P<server_id>\d+)/characters$', CharactersView.as_view()),
	url(r'^(?P<server_id>\d+)/characters/(?P<character_id>\d+)$', CharacterView.as_view())
]

from django.urls import path

from .views import (CharacterHistoryView, CharactersView, CharacterView,
                    ClansView, ClanView, ServersView, ServerView,
                    SyncCharactersView, ClanCharactersView, ActiveClansView,
                    ServerInfoView)

urlpatterns = [
    path(r'', ServersView.as_view()),
    path(r'widgets/serverinfo/', ServerInfoView.as_view()),
    path(r'<int:server_id>/', ServerView.as_view()),
    path(r'<int:server_id>/sync/characters/', SyncCharactersView.as_view()),
    path(r'<int:server_id>/clans/', ClansView.as_view()),
    path(r'<int:server_id>/clans/<int:clan_id>/', ClanView.as_view()),
    path(r'<int:server_id>/clans/<int:clan_id>/characters/', ClanCharactersView.as_view()),
    path(r'<int:server_id>/characters/', CharactersView.as_view()),
    path(r'<int:server_id>/characters/<int:character_id>/', CharacterView.as_view()),
    path(r'<int:server_id>/characters/<int:character_id>/history/', CharacterHistoryView.as_view()),
    path(r'<int:server_id>/widgets/activeclans/', ActiveClansView.as_view()),
]

from .base import BaseAdminView
from api.models import Character, Server, CharacterHistory
from datetime import datetime, timedelta
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone
import json
import pytz
from api.plugins.ginfo import GinfoPlugin

class SyncCharactersView(BaseAdminView):
    ginfoPlugin = GinfoPlugin()

    def post(self, request, server_id):
        now = timezone.now()

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
            history_buffer = []

            # Delete removed characters
            synced_ids = [c['conan_id'] for c in data['characters']]

            (Character.objects
                .filter(server=server)
                .filter(~Q(conan_id__in=synced_ids))
                .delete())

            for sync_data in data['characters']:
                character = (Character.objects
                    .filter(conan_id=sync_data['conan_id'])
                    .first())

                if character is None:
                    character = Character()

                has_no_changes = (
                    (sync_data['x'] == character.x) or
                    (sync_data['y'] == character.y) or
                    (sync_data['z'] == character.y))

                last_online = (datetime
                    .utcfromtimestamp(sync_data['last_online'])
                    .replace(tzinfo=pytz.utc))

                character.server         = server
                character.conan_id       = sync_data['conan_id']
                character.name           = sync_data['name']
                character.level          = sync_data['level']
                character.is_online      = sync_data['is_online']
                character.steam_id       = sync_data['steam_id']
                character.last_killed_by = sync_data['last_killed_by']
                character.x              = sync_data['x']
                character.y              = sync_data['y']
                character.z              = sync_data['z']
                character.last_online    = last_online
                character.save()

                if not has_no_changes:
                    history_buffer.append(CharacterHistory(
                        character=character,
                        created=now,
                        x=character.x,
                        y=character.y,
                        z=character.z))
                    if 'ginfo_group_uid' in request.GET and 'ginfo_access_token' in request.GET:
                        try:
                            self.ginfoPlugin.update_position(character, request.GET['ginfo_group_uid'], request.GET['ginfo_access_token'])
                        except:
                            # TODO: Error Loggin / NewRelic?
                            pass

            # speed up history creation by creating in bulk
            CharacterHistory.objects.bulk_create(history_buffer)

        # Delete history older than 5 days
        history_threshold = timezone.now() - timedelta(days=5)
        CharacterHistory.objects.filter(created__lt=history_threshold).delete()



        server.last_sync = now
        server.save()
        return HttpResponse(status=200)

from api.models import Character
from api.plugins.ginfo import GinfoPlugin


def sync_ginfo(character_ids, group_uid, access_token):
    characters = (Character.objects
        .filter(id__in=character_ids)
        .order_by('id'))

    plugin = GinfoPlugin()

    for character in characters:
        plugin.update_position(character, group_uid, access_token)

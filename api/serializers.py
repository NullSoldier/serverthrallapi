import calendar
from api.models import Character

import serpy


class EnumField(serpy.Field):

    def to_value(self, v):
        return v.name


class DatetimeToUnixField(serpy.Field):

    def to_value(self, v):
        if v is None:
            return None
        return calendar.timegm(v.utctimetuple())

class CharacterLocationField(serpy.Field):

    getter_takes_serializer = True

    def as_getter(self, serializer_field_name, serializer_cls):
        return lambda self, v: {'x': v.x, 'y': v.y, 'z': v.z}


class ClanSerializer(serpy.Serializer):
    id              = serpy.Field()
    server_id       = serpy.Field()
    name            = serpy.Field()
    motd            = serpy.Field()
    owner_id        = serpy.Field()
    owner_name      = serpy.MethodField()
    character_count = serpy.Field()
    created         = DatetimeToUnixField()
    active_count    = serpy.MethodField()

    def get_active_count(self, item):
        return item.active_count if item.active_count else 0

    def get_owner_name(self, item):
        return item.owner.name if item.owner is not None else None


class CharacterSerializer(serpy.Serializer):
    id             = serpy.Field()
    server_id      = serpy.Field()
    steam_id       = serpy.Field()
    clan_id        = serpy.Field()
    name           = serpy.Field()
    level          = serpy.Field()
    is_online      = serpy.Field()
    clan_name      = serpy.MethodField()
    created        = DatetimeToUnixField()
    last_online    = DatetimeToUnixField()
    last_killed_by = serpy.Field()

    def get_clan_name(self, item):
        return item.clan.name if item.clan is not None else None


class CharacterHistorySerializer(serpy.Serializer):
    character_id   = serpy.Field()
    created        = DatetimeToUnixField()


class ServerSerializer(serpy.Serializer):
    id              = serpy.Field()
    name            = serpy.Field()
    character_count = serpy.Field()
    online_count    = serpy.MethodField()
    ip_address      = serpy.Field()
    query_port      = serpy.Field()
    tick_rate       = serpy.Field()
    max_players     = serpy.Field()
    version         = serpy.Field()
    last_sync       = DatetimeToUnixField()

    def get_online_count(self, server):
        return Character.objects.filter(server=server, is_online=True).count()


class ServerAdminSerializer(ServerSerializer):
    private_secret  = serpy.Field()

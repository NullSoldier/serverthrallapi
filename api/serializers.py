import serpy
import calendar


class EnumField(serpy.Field):

    def to_value(self, v):
        return v.name


class DatetimeToUnixField(serpy.Field):

    def to_value(self, v):
        if v is None:
            return None
        return calendar.timegm(v.utctimetuple())


class CharacterSerializer(serpy.Serializer):
	id             = serpy.Field()
	server_id      = serpy.Field()
	name           = serpy.Field()
	level          = serpy.Field()
	is_online      = serpy.Field()
	steam_id       = serpy.Field()
	conan_id       = serpy.Field()
	last_online    = DatetimeToUnixField()
	last_killed_by = serpy.Field()
	x              = serpy.Field()
	y              = serpy.Field()
	z              = serpy.Field()


class ServerAdminSerializer(serpy.Serializer):
	id             = serpy.Field()
	name           = serpy.Field()
	private_secret = serpy.Field()
	last_sync      = DatetimeToUnixField()

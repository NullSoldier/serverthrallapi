import serpy


class CharacterSerializer(serpy.Serializer):
	id                = serpy.Field()
	server_id         = serpy.Field()
	name              = serpy.Field()
	level             = serpy.Field()
	is_online         = serpy.Field()
	steam_id          = serpy.Field()
	conan_id          = serpy.Field()
	last_online       = serpy.Field()
	last_killed_by_id = serpy.Field()
	x                 = serpy.Field()
	y                 = serpy.Field()
	z                 = serpy.Field()
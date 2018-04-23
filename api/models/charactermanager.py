from django.db import models


class CharacterManager(models.QuerySet):

    def with_clan_name(self):
        return self.extra(select={'clan_name': 'select name from api_clan where api_clan.conan_id = api_character.conan_clan_id'})

from django.db import models


class ClanManager(models.QuerySet):

    def with_character_count(self):
        return self.extra(select={'character_count': '''
            select count(api_character.id)
            from api_character
            where
                (api_character.conan_clan_id = api_clan.conan_id) and
                (api_character.server_id = api_clan.server_id)'''})

    def with_owner_name(self):
        return self.extra(select={'owner_name': '''
            select api_character.name
            from api_character
            where
                (api_character.conan_id = api_clan.owner_id) and
                (api_character.server_id = api_clan.server_id)
            limit 1'''})

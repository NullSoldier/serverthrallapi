from django.db import models
from django.db.models import Count


class ClanManager(models.QuerySet):

    def with_character_count(self):
        return self.annotate(character_count=Count('members'))

from django.db import models
from django.db.models import Count, Max, OuterRef, Subquery
from datetime import datetime, timedelta


class ClanManager(models.QuerySet):

    def with_character_count(self):
        return self.annotate(character_count=Count('members'))

    def with_last_logged_in(self):
        return self.annotate(last_logged_in=Max('members__last_online'))

    def with_active_count(self):
        from api.models import Character

        active_query = (Character.objects
            .active_only()
            .filter(clan=OuterRef('id'))
            .values('clan_id')
            .order_by()
            .annotate(count=Count('*'))
            .values('count')[:1])

        return self.annotate(active_count=Subquery(
            active_query, output_field=models.IntegerField()))

    def active_only(self):
        return (self.with_last_logged_in().filter(
            last_logged_in__gt=datetime.now() - timedelta(days=7)))

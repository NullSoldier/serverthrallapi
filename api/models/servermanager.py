from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, OuterRef, Subquery


class ServerManager(models.QuerySet):

    def only_active(self):
        active_threshold = timezone.now() - timedelta(days=2)

        return self.filter(
            last_sync__gt=active_threshold,
            last_sync__isnull=False)

    def with_character_count(self):
        return self.annotate(character_count=Count('characters'))

    def with_online_count(self):
        from api.models import Character

        count_online = (Character.objects
            .filter(server=OuterRef('pk'))
            .order_by()
            .values('server')
            .annotate(count=Count('*'))
            .values('count'))

        return self.annotate(online_count=Subquery(count_online))

from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count


class ServerManager(models.QuerySet):

    def only_active(self):
        active_threshold = timezone.now() - timedelta(days=2)

        return self.filter(
            last_sync__gt=active_threshold,
            last_sync__isnull=False)

    def with_character_count(self):
        return self.annotate(character_count=Count('characters'))

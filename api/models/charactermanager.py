from django.db import models
from datetime import datetime, timedelta

class CharacterManager(models.QuerySet):

    def active_only(self):
        return self.filter(last_online__gt=datetime.now() - timedelta(days=7))

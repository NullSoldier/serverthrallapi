from django.db import models

from api.models import Character


class GinfoCharacter(models.Model):
    character = models.ForeignKey(
        Character,
        related_name="ginfo_character",
        related_query_name="ginfo_character",
    )
    ginfo_marker_uid = models.TextField()

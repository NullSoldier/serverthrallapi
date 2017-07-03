from django.db import models
from api.models import Character


class GInfoCharacter(models.Model):
    character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name="ginfo_character",
        related_query_name="ginfo_character",
    )
    ginfo_marker_uid = models.TextField()

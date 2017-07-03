from django.db import models
from api.models import Character


class GInfoCharacter(models.Model):
    character = models.ForeignKey(Character)
    ginfo_marker_uid = models.TextField()

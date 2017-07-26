from django.db import models


class CharacterHistory(models.Model):
    created           = models.DateTimeField(auto_now_add=True)
    character         = models.ForeignKey('api.Character')
    x                 = models.FloatField()
    y                 = models.FloatField()
    z                 = models.FloatField()

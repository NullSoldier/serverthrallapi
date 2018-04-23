from django.db import models
from .charactermanager import CharacterManager


class Character(models.Model):
    name           = models.TextField()
    level          = models.IntegerField()
    is_online      = models.BooleanField()
    steam_id       = models.TextField()
    conan_id       = models.TextField()
    conan_clan_id  = models.TextField(null=True)
    last_online    = models.DateTimeField(null=True)
    last_killed_by = models.TextField(null=True)
    created        = models.DateTimeField(auto_now_add=True)
    server         = models.ForeignKey('api.Server', related_name='characters')
    x              = models.FloatField()
    y              = models.FloatField()
    z              = models.FloatField()

    objects = CharacterManager.as_manager()

    def generate_history(self, created):
        from .characterhistory import CharacterHistory
        return CharacterHistory(
            character=self,
            created=created,
            x=self.x,
            y=self.y,
            z=self.z)

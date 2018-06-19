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
    clan           = models.ForeignKey('api.Clan', related_name='members', null=True, on_delete=models.DO_NOTHING)
    server         = models.ForeignKey('api.Server', related_name='characters', on_delete=models.DO_NOTHING)
    x              = models.FloatField(null=True)
    y              = models.FloatField(null=True)
    z              = models.FloatField(null=True)

    objects = CharacterManager.as_manager()

    def generate_history(self, created):
        from .characterhistory import CharacterHistory
        return CharacterHistory(
            character=self,
            created=created,
            x=self.x,
            y=self.y,
            z=self.z)

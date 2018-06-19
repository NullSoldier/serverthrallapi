from django.db import models
from .clanmanager import ClanManager


class Clan(models.Model):
    name           = models.TextField()
    conan_id       = models.TextField()
    conan_owner_id = models.TextField()
    motd           = models.TextField()
    created        = models.DateTimeField(auto_now_add=True)
    owner          = models.ForeignKey('api.Character', related_name='owner', null=True, on_delete=models.DO_NOTHING)
    server         = models.ForeignKey('api.Server', related_name='clans', on_delete=models.DO_NOTHING)

    objects = ClanManager.as_manager()

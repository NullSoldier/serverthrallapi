from django.db import models
from .servermanager import ServerManager


class Server(models.Model):
    private_secret = models.UUIDField()
    last_sync      = models.DateTimeField(null=True)
    sync_rcon      = models.BooleanField(default=False)
    rcon_host      = models.TextField(null=True)
    rcon_port      = models.IntegerField(null=True)
    rcon_password  = models.TextField(null=True)
    name           = models.TextField(null=True)
    ip_address     = models.TextField(null=True)
    version        = models.TextField(null=True)
    query_port     = models.TextField(null=True)
    max_players    = models.IntegerField(null=True)
    tick_rate      = models.IntegerField(null=True)

    objects = ServerManager.as_manager()

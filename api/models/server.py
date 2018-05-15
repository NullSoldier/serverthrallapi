from django.db import models
from .servermanager import ServerManager


class Server(models.Model):
    name           = models.TextField()
    ip_address     = models.TextField(default='')
    version        = models.TextField(null=True)
    query_port     = models.TextField(null=True)
    max_players    = models.IntegerField(null=True)
    tick_rate      = models.IntegerField(null=True)
    private_secret = models.UUIDField()
    last_sync      = models.DateTimeField(null=True)

    objects = ServerManager.as_manager()

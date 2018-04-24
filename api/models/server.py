from django.db import models
from .servermanager import ServerManager


class Server(models.Model):
    name           = models.TextField()
    ip_address     = models.TextField(default='')
    private_secret = models.UUIDField()
    last_sync      = models.DateTimeField(null=True)

    objects = ServerManager.as_manager()

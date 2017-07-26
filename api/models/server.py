from django.db import models


class Server(models.Model):
    name           = models.TextField()
    private_secret = models.UUIDField()
    last_sync      = models.DateTimeField(null=True)

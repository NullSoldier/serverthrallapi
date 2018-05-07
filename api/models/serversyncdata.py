from django.db import models


class ServerSyncData(models.Model):
    server  = models.ForeignKey('api.Server', related_name='+')
    data    = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

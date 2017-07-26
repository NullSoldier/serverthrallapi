from django.db import models


class Clan(models.Model):
    name     = models.TextField()
    conan_id = models.TextField()
    owner_id = models.TextField()
    motd     = models.TextField()
    created  = models.DateTimeField(auto_now_add=True)
    server   = models.ForeignKey('api.Server')

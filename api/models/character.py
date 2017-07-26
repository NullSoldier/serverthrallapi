from django.db import models


class Character(models.Model):
    name              = models.TextField()
    level             = models.IntegerField()
    is_online         = models.BooleanField()
    steam_id          = models.TextField()
    conan_id          = models.TextField()
    last_online       = models.DateTimeField(null=True)
    last_killed_by    = models.TextField(null=True)
    created           = models.DateTimeField(auto_now_add=True)
    server            = models.ForeignKey('api.Server')
    x                 = models.FloatField()
    y                 = models.FloatField()
    z                 = models.FloatField()

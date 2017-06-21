from __future__ import unicode_literals
from django.db import models

# 357d50b1-5635-11e7-b108-e03f497a3b2c

class Character(models.Model):
	name           = models.TextField()
	level          = models.IntegerField(default=0)
	is_online      = models.BooleanField(default=False)
	steam_id       = models.TextField()
	conan_id       = models.TextField()
	last_online    = models.DateTimeField()
	last_killed_by = models.ForeignKey('api.Character', null=True)
	server         = models.ForeignKey('api.Server')
	x              = models.FloatField()
	y              = models.FloatField()
	z              = models.FloatField()


class Server(models.Model):
	name           = models.TextField()
	public_secret  = models.UUIDField()
	private_secret = models.UUIDField()
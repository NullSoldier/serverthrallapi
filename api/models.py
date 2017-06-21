from __future__ import unicode_literals
from django.db import models

class Character(models.Model):
	name           = models.TextField()
	level          = models.IntegerField(default=0)
	is_online      = models.BooleanField(default=False)
	steam_id       = models.TextField()
	conan_id       = models.TextField()
	last_online    = models.DatetimeField()
	last_killed_by = models.ForeignKey(Character)
	x              = models.FloatField()
	y              = models.FloatField()
	z              = models.FloatField()
from django.db import models


class Server(models.Model):
	name           = models.TextField()
	public_secret  = models.UUIDField()
	private_secret = models.UUIDField()
	last_sync      = models.DateTimeField(null=True)
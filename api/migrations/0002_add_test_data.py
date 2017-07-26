# flake8: noqa
from __future__ import unicode_literals

import uuid
from datetime import datetime

from django.db import migrations
from django.utils import timezone


def add_data(apps, schema_editor):
	Server = apps.get_model('api', 'Server')
	Character = apps.get_model('api', 'Character')

	server =  Server.objects.create(
		name='Test Server',
		public_secret=uuid.uuid1(),
		private_secret=uuid.uuid1())

	char1 = Character.objects.create(
		name='NullSoldier',
		level=5,
		is_online=False,
		steam_id=76561197963906761,
		conan_id=1,
		last_online=timezone.now(),
		last_killed_by='',
		created=timezone.now(),
		server=server,
		x=0,
		y=0,
		z=0)

	char2 = Character.objects.create(
		name='Immotal',
		level=8,
		is_online=True,
		steam_id=76561197984850480,
		conan_id=2,
		last_online=timezone.now(),
		last_killed_by='',
		created=timezone.now(),
		server=server,
		x=0,
		y=0,
		z=0)

	print server.private_secret


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
    	migrations.RunPython(add_data)
    ]

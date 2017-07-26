# flake8: noqa
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_server_public_secret'),
    ]

    operations = [
        migrations.CreateModel(
            name='CharacterHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('z', models.FloatField()),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Character')),
            ],
        ),
    ]

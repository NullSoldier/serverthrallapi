# flake8: noqa
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_characterhistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='GinfoCharacter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ginfo_marker_uid', models.TextField()),
                ('character', models.ForeignKey(related_name='ginfo_character', related_query_name='ginfo_character', to='api.Character')),
            ],
        ),
    ]

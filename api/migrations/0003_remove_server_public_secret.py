# flake8: noqa
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_add_test_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='public_secret',
        ),
    ]

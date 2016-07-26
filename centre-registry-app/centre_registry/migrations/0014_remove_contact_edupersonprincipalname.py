# pylint: disable=invalid-name
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [('centre_registry', '0013_auto_20150424_1553'), ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='edupersonprincipalname', ),
    ]

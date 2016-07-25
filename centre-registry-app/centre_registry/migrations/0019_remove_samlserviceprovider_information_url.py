# pylint: disable=invalid-name
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [('centre_registry', '0018_auto_20150429_1632'), ]

    operations = [
        migrations.RemoveField(model_name='samlserviceprovider',
                               name='information_url', ),
    ]

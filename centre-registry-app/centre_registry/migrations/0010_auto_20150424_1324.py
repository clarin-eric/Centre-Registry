# pylint: disable=invalid-name
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [('centre_registry', '0009_auto_20150423_1526'), ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='website',
            new_name='website_url', ),
    ]

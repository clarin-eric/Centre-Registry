# pylint: disable=invalid-name
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [('centre_registry', '0008_auto_20150423_1520'), ]

    operations = [
        migrations.AlterModelOptions(
            name='urlreference',
            options={'verbose_name': 'URL reference',
                     'verbose_name_plural':
                     'URL references',
                     'ordering': ('url', )}, ),
    ]

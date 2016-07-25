# pylint: disable=invalid-name
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [('centre_registry', '0012_auto_20150424_1546'), ]

    operations = [
        migrations.AlterField(model_name='consortium',
                              name='name',
                              field=models.CharField(max_length=40,
                                                     verbose_name='Name',
                                                     blank=True), ),
    ]

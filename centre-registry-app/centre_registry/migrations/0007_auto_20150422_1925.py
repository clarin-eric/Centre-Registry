# pylint: disable=invalid-name
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [('centre_registry', '0006_auto_20150422_1920'), ]

    operations = [
        migrations.AlterField(model_name='samlserviceprovider',
                              name='production_status',
                              field=models.BooleanField(
                                  default=True,
                                  verbose_name='Has production status?'), ),
    ]

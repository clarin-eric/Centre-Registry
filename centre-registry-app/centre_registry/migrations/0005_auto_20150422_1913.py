# pylint: disable=invalid-name
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [('centre_registry', '0004_auto_20150422_1906'), ]

    operations = [
        migrations.AddField(
            model_name='samlserviceprovider',
            name='information_url',
            field=models.URLField(
                verbose_name='Information URL', max_length=1024,
                blank=True), ),
        migrations.AddField(
            model_name='samlserviceprovider',
            name='production_status',
            field=models.BooleanField(
                default=True, verbose_name='Has production status?'),
            preserve_default=False, ),
    ]

# Generated by Django 2.2.8 on 2019-12-18 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centre_registry', '0002_auto_20191216_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='centre',
            name='organisation_name',
            field=models.CharField(max_length=100, verbose_name='Organisation'),
        ),
    ]
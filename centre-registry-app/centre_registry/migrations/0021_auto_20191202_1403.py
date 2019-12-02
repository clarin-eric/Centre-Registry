# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-12-02 14:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('centre_registry', '0020_auto_20170118_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='fcsendpoint',
            name='note',
            field=models.CharField(blank=True, max_length=1024, verbose_name='Additional note'),
        ),
        migrations.AddField(
            model_name='oaipmhendpoint',
            name='note',
            field=models.CharField(blank=True, max_length=1024, verbose_name='Additional note'),
        ),
        migrations.AddField(
            model_name='samlserviceprovider',
            name='note',
            field=models.CharField(blank=True, max_length=1024, verbose_name='Additional note'),
        ),
        migrations.AlterField(
            model_name='assessmentdates',
            name='duedate',
            field=models.DateField(verbose_name='Assessment due date (YYYY-MM-DD)'),
        ),
        migrations.AlterField(
            model_name='assessmentdates',
            name='issuedate',
            field=models.DateField(verbose_name='Assessment issued date (YYYY-MM-DD)'),
        ),
        migrations.AlterField(
            model_name='assessmentdates',
            name='type',
            field=models.ManyToManyField(to='centre_registry.CentreType', verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='fcsendpoint',
            name='centre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='centre_registry.Centre'),
        ),
        migrations.AlterField(
            model_name='oaipmhendpoint',
            name='centre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='centre_registry.Centre'),
        ),
        migrations.AlterField(
            model_name='samlserviceprovider',
            name='centre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='centre_registry.Centre'),
        ),
        migrations.AlterField(
            model_name='samlserviceprovider',
            name='entity_id',
            field=models.URLField(max_length=1024, unique=True, verbose_name='Entity ID'),
        ),
        migrations.AlterField(
            model_name='samlserviceprovider',
            name='status_url',
            field=models.CharField(blank=True, max_length=1024, verbose_name='Status URL'),
        ),
    ]
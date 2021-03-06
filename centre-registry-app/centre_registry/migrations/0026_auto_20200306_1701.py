# Generated by Django 2.2.8 on 2020-03-06 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centre_registry', '0025_auto_20200122_1858'),
       ]

    operations = [
        migrations.CreateModel(
            name='OAIPMHEndpointSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('set_spec', models.CharField(max_length=1024, verbose_name='Set specification')),
                ('set_type', models.CharField(max_length=1024, null=True, verbose_name='Set type')),
            ],
            options={
                'verbose_name': 'OAI-PMH endpoint specification',
                'verbose_name_plural': 'OAI-PMH endpoint specifications',
                'ordering': ('set_spec', 'set_type'),
            },
        ),
        migrations.AddField(
            model_name='oaipmhendpoint',
            name='oai_pmh_sets',
            field=models.ManyToManyField(blank=True, related_name='web_services', to='centre_registry.OAIPMHEndpointSet'),
        ),
    ]

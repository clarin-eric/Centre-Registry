# Generated by Django 4.2.18 on 2025-02-12 16:19

from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('centre_registry', '0040_rename_type_status_centre_type_status_comment_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CertificationStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=30, verbose_name='Certification status')),
            ],
        ),
        migrations.AddField(
            model_name='centre',
            name='requires_manual_certificate_validation',
            field=models.BooleanField(default=False, verbose_name='Centre requires certificate status validation'),
        ),
        migrations.AddField(
            model_name='historicalcentre',
            name='requires_manual_certificate_validation',
            field=models.BooleanField(default=False, verbose_name='Centre requires certificate status validation'),
        ),
        migrations.AddField(
            model_name='centre',
            name='type_certification_status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='centre_registry.certificationstatus'),
        ),
        migrations.AddField(
            model_name='historicalcentre',
            name='type_certification_status',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='centre_registry.certificationstatus'),
        ),
        migrations.CreateModel(
            name='HistoricalCertificationStatus',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('status', models.CharField(max_length=30, verbose_name='Certification status')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical certification status',
                'verbose_name_plural': 'historical certification statuss',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]

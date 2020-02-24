# Generated by Django 2.2.8 on 2020-01-22 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('centre_registry', '0023_auto_20191216_1202'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assessmentdates',
            options={'ordering': ('issuedate', 'duedate'), 'verbose_name': 'issue/due dates for a centre administrative_contacttype', 'verbose_name_plural': 'issue/due dates for a centre type'},
        ),
        migrations.AlterField(
            model_name='centre',
            name='consortium',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='centre_registry.Consortium'),
        ),
        migrations.AlterField(
            model_name='centre',
            name='technical_contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='technical_contact', to='centre_registry.Contact'),
        ),
    ]
# Generated by Django 4.0.6 on 2022-08-05 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0001_initial'),
        ('schedule', '0010_remove_schedule_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='location',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='location.location'),
        ),
    ]

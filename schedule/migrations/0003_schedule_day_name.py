# Generated by Django 4.0.6 on 2022-08-01 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_alter_schedule_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='day_name',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
# Generated by Django 4.0.6 on 2022-08-01 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_alter_schedule_day_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='day_name',
            field=models.CharField(auto_created=True, default='WED', editable=False, max_length=10),
        ),
    ]

# Generated by Django 4.0.6 on 2022-07-27 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('doctors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('start', models.TimeField(null=True)),
                ('end', models.TimeField(null=True)),
                ('lunch_start', models.TimeField(null=True)),
                ('lunch_end', models.TimeField(null=True)),
                ('doctor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='doctors.doctor')),
            ],
        ),
    ]

# Generated by Django 4.0.6 on 2022-07-27 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('location', '0001_initial'),
        ('doctors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('last_name', models.CharField(max_length=150, null=True)),
                ('date', models.DateField(help_text='Date format yyyy-mm-dd.')),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctors.doctor')),
                ('location', models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='location.location')),
            ],
        ),
    ]

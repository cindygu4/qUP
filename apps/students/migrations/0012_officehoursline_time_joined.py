# Generated by Django 3.0.7 on 2020-08-19 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0011_auto_20200818_1954'),
    ]

    operations = [
        migrations.AddField(
            model_name='officehoursline',
            name='time_joined',
            field=models.TimeField(null=True),
        ),
    ]

# Generated by Django 3.0.7 on 2020-08-15 01:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0004_auto_20200815_0105'),
    ]

    operations = [
        migrations.RenameField(
            model_name='queue',
            old_name='start_date',
            new_name='date',
        ),
    ]

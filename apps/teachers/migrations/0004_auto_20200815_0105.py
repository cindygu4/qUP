# Generated by Django 3.0.7 on 2020-08-15 01:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0003_auto_20200815_0103'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='queue',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='queue',
            name='frequency',
        ),
    ]

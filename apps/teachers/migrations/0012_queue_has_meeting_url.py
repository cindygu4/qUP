# Generated by Django 3.0.7 on 2020-08-17 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0011_queue_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='has_meeting_url',
            field=models.BooleanField(default=False),
        ),
    ]

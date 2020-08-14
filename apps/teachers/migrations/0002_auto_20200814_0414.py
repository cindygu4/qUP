# Generated by Django 3.0.7 on 2020-08-14 04:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teachers', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='students',
            field=models.ManyToManyField(related_name='classrooms', to='users.Student'),
        ),
        migrations.AddField(
            model_name='classroom',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classrooms', to='users.Teacher'),
        ),
    ]

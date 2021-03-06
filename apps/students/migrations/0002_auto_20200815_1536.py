# Generated by Django 3.0.7 on 2020-08-15 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0005_auto_20200815_0109'),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])),
                ('comments', models.TextField()),
                ('queue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='teachers.Queue')),
            ],
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
    ]

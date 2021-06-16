# Generated by Django 3.2.3 on 2021-06-15 09:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('data_visualization', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data_set',
            name='time',
            field=models.DateTimeField(default='2021-06-15T11:24:46.146610'),
        ),
        migrations.AlterField(
            model_name='data_set',
            name='user_id',
            field=models.UUIDField(default=uuid.UUID('8658a1f7-cdbb-11eb-94e4-b89a2a687c94')),
        ),
    ]

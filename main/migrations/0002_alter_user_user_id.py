# Generated by Django 3.2.3 on 2021-06-15 09:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.CharField(default=uuid.UUID('8658a1f7-cdbb-11eb-94e4-b89a2a687c94'), max_length=255),
        ),
    ]

# Generated by Django 3.2.3 on 2021-06-09 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20210607_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data_set',
            name='time',
            field=models.DateTimeField(default='2021-06-09T15:28:42.833513'),
        ),
        migrations.AlterField(
            model_name='data_set',
            name='user_id',
            field=models.CharField(default='9c032d90-c926-11eb-b01b-b89a2a687c97', max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.CharField(default='9c032d90-c926-11eb-b01b-b89a2a687c97', max_length=255),
        ),
    ]
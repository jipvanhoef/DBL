# Generated by Django 3.2.3 on 2021-06-11 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_auto_20210610_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data_set',
            name='time',
            field=models.DateTimeField(default='2021-06-11T09:38:12.223601'),
        ),
        migrations.AlterField(
            model_name='data_set',
            name='user_id',
            field=models.CharField(default='f99e60cf-ca87-11eb-8bd6-b89a2a687c97', max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.CharField(default='f99e60cf-ca87-11eb-8bd6-b89a2a687c97', max_length=255),
        ),
    ]

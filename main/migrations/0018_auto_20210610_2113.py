# Generated by Django 3.2.3 on 2021-06-10 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20210610_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data_set',
            name='time',
            field=models.DateTimeField(default='2021-06-10T21:13:37.911998'),
        ),
        migrations.AlterField(
            model_name='data_set',
            name='user_id',
            field=models.CharField(default='f5a76f6e-ca1f-11eb-9dc6-b89a2a687c97', max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.CharField(default='f5a76f6e-ca1f-11eb-9dc6-b89a2a687c97', max_length=255),
        ),
    ]
# Generated by Django 3.2.3 on 2021-06-07 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20210604_1400'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default='6a894adc-c788-11eb-9f1a-b89a2a687c97', max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='data_set',
            name='time',
            field=models.DateTimeField(default='2021-06-07T14:03:48.180423'),
        ),
        migrations.AlterField(
            model_name='data_set',
            name='user_id',
            field=models.CharField(default='6a894adc-c788-11eb-9f1a-b89a2a687c97', max_length=255),
        ),
    ]

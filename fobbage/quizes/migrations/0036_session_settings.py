# Generated by Django 3.1.7 on 2021-04-18 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizes', '0035_auto_20210415_2044'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='settings',
            field=models.JSONField(default=dict),
        ),
    ]

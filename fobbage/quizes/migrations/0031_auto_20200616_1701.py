# Generated by Django 3.0.4 on 2020-06-16 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizes', '0030_auto_20200616_1655'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='Quiz',
            new_name='quiz',
        ),
    ]

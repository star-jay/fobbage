# Generated by Django 3.0.4 on 2020-06-15 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizes', '0028_auto_20200615_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='modus',
            field=models.IntegerField(choices=[(0, 'Bluffing'), (1, 'Guessing')], default=0),
        ),
    ]

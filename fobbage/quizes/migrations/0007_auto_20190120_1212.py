# Generated by Django 2.1.4 on 2019-01-20 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizes', '0006_auto_20181220_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='status',
            field=models.IntegerField(choices=[(0, 'Inactive'), (1, 'Bluff'), (2, 'Guess'), (3, 'Finished')], default=0),
        ),
        migrations.AddField(
            model_name='round',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]

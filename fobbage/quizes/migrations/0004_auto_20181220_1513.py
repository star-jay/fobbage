# Generated by Django 2.1.3 on 2018-12-20 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizes', '0003_auto_20181204_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='round',
            name='multiplier',
            field=models.FloatField(default=1),
        ),
    ]

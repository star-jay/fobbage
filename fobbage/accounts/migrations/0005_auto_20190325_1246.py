# Generated by Django 2.1.5 on 2019-03-25 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20190325_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True, verbose_name='email address'),
        ),
    ]

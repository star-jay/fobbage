# Generated by Django 2.1.5 on 2019-01-25 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizes', '0014_answer_showed'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 2.1.5 on 2019-03-25 15:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quizes', '0016_question_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='quiz',
            name='players',
            field=models.ManyToManyField(related_name='quizes_playing', to=settings.AUTH_USER_MODEL),
        ),
    ]

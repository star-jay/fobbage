# Generated by Django 2.1.3 on 2018-12-20 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizes', '0004_auto_20181220_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='quizes.Question'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='answer',
            name='text',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]

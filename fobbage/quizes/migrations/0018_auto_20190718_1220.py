# Generated by Django 2.2.3 on 2019-07-18 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizes', '0017_auto_20190325_1512'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='round',
            name='active_question',
        ),
        migrations.RemoveField(
            model_name='round',
            name='is_active',
        ),
        migrations.AddField(
            model_name='quiz',
            name='active_question',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='quizes.Question'),
        ),
    ]
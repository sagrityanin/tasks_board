# Generated by Django 4.1.4 on 2022-12-27 16:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='task',
            name='task_is_comp_3cfb65_idx',
        ),
        migrations.RemoveField(
            model_name='task',
            name='is_completed',
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.TextField(choices=[('created', 'created'), ('executed', 'executed'), ('deprecated', 'deprecated')], default='created', verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='user',
            name='note_chanal',
            field=models.TextField(choices=[('telegramm', 'telegramm')], default='telegramm', verbose_name='NoteChanal'),
        ),
        migrations.AlterField(
            model_name='task',
            name='id',
            field=models.UUIDField(default=uuid.UUID('b73c1f7f-52b2-402d-bae2-426104a8d227'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.UUID('b73c1f7f-52b2-402d-bae2-426104a8d227'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['status', 'creator_id', 'executor_id'], name='task_status_678c32_idx'),
        ),
    ]
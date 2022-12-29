# Generated by Django 4.1.4 on 2022-12-28 05:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_status_and_more'),
    ]

    operations = [
        migrations.RenameIndex(
            model_name='task',
            new_name='task_status_678c32_idx',
            old_name='task_status__907d71_idx',
        ),
        migrations.AlterField(
            model_name='task',
            name='id',
            field=models.UUIDField(default=uuid.UUID('80ba5ed4-f751-46a0-8d57-5e4fda86c2bd'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.TextField(choices=[('created', 'created'), ('executed', 'executed'), ('deprecated', 'deprecated')], default='created', verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.UUID('80ba5ed4-f751-46a0-8d57-5e4fda86c2bd'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.DeleteModel(
            name='Status',
        ),
    ]
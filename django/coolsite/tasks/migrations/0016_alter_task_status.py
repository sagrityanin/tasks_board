# Generated by Django 4.1.4 on 2022-12-28 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0015_rename_time_create_task_time_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.TextField(choices=[('created', 'created'), ('executed', 'executed'), ('deprecated', 'deprecated')], default='created', verbose_name='Status'),
        ),
    ]

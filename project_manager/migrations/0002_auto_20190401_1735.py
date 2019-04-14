# Generated by Django 2.1.7 on 2019-04-01 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_manager', '0001_initial'),
        ('project_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('finish_time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='task',
            name='finish_time',
        ),
        migrations.RemoveField(
            model_name='task',
            name='start_time',
        ),
        migrations.AddField(
            model_name='project',
            name='instructor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects', to='user_manager.Instructor'),
        ),
        migrations.AddField(
            model_name='project',
            name='students',
            field=models.ManyToManyField(related_name='projects', to='user_manager.Student'),
        ),
        migrations.AddField(
            model_name='task',
            name='members',
            field=models.ManyToManyField(related_name='tasks', to='user_manager.Student'),
        ),
        migrations.AddField(
            model_name='task',
            name='project',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='project_manager.Project'),
        ),
        migrations.AddField(
            model_name='timelog',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='project_manager.Task'),
        ),
        migrations.AddField(
            model_name='timelog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='user_manager.Student'),
        ),
    ]
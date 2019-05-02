import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yatracker.settings")
django.setup()
from project_manager.models import *
from user_manager.models import *
from datetime import datetime
import pytz

temur = User.objects.get(name="Temur")
danil = User.objects.get(name="Danil")
rishat = User.objects.get(name="Rishat")
susanna = User.objects.get(name="Susanna")
elena = User.objects.get(name="Elena")


def run():
    project = Project.objects.get(title="Time Tracking System")

    TimeLog.objects.filter(task__project=project).delete()
    Task.objects.filter(project=project).delete()

    # 4
    task1 = Task(
        title='Statistics Page',
        description='As a developer, I want to use the Dash Plotly framework so that I can create beautiful graphs with statistics.',
        status='done',
        project=project
    )
    task1.save()
    # 1
    task2 = Task(
        title='Change Instructors',
        description='Add our instructor to the projects',
        status='done',
        project=project
    )
    task2.save()
    # 3
    task3 = Task(
        title='Fix the add/delete students functionality',
        description='As an instructor, I want to have special buttons so that I can add or delete students to/from a project.',
        status='done',
        project=project
    )
    task3.save()
    # 2
    task4 = Task(
        title='Fix the bug with unlimited length of texts',
        description='Fix the view and problem with too long texts in task description',
        status='done',
        project=project
    )
    task4.save()

    task5 = Task(
        title='Add a search field to the modification page',
        description='As an instructor, I want to have a search field with filtering (by surname, ID, etc.) so that I can look for students to add them in a team.',
        status='todo',
        project=project
    )
    task5.save()
    # 5
    task6 = Task(
        title='Organize the project board',
        description='Fulfill the project board with tasks and add timelogs for statistics.',
        status='paus',
        project=project
    )
    task6.save()

    task7 = Task(
        title='Make a presentation',
        description='Make a final presentation of the project.',
        status='todo',
        project=project
    )
    task7.save()
    # 26-27 + 1.05 4 hours
    timelog1_1 = TimeLog(
        user=temur,
        task=task1,
        start_time=datetime(2019, 4, 26, 21, 21, 00, tzinfo=pytz.UTC),
        finish_time=datetime(2019, 4, 26, 22, 45, 00, tzinfo=pytz.UTC)
    )
    timelog1_1.save()

    timelog1_2 = TimeLog(
        user=rishat,
        task=task1,
        start_time=datetime(2019, 4, 27, 16, 21, 00, tzinfo=pytz.UTC),
        finish_time=datetime(2019, 4, 27, 18, 32, 00, tzinfo=pytz.UTC)
    )
    timelog1_2.save()

    timelog1_3 = TimeLog(
        user=temur,
        task=task1,
        start_time=datetime(2019, 5, 1, 16, 21, 00, tzinfo=pytz.UTC),
        finish_time=datetime(2019, 5, 1, 16, 59, 00, tzinfo=pytz.UTC)
    )
    timelog1_3.save()

    #45 mins
    timelog2 = TimeLog(
        user=temur,
        task=task2,
        # 21 04 19
        start_time=datetime(2019, 4, 21, 16, 13, 00, tzinfo=pytz.UTC),
        finish_time=datetime(2019, 4, 21, 16, 56, 00, tzinfo=pytz.UTC)
    )
    timelog2.save()

    timelog3 = TimeLog(
        user=danil,
        task=task3,
        # 24-25 04 2 hours
        start_time=datetime(2019, 4, 24, 22, 49, 00, tzinfo=pytz.UTC),
        finish_time=datetime(2019, 4, 25, 0, 55, 00, tzinfo=pytz.UTC)
    )
    timelog3.save()

    timelog4 = TimeLog(
        user=temur,
        task=task4,
        # 22 04 19 1 hour
        start_time=datetime(2019, 4, 22, 18, 39, 00, tzinfo=pytz.UTC),
        finish_time=datetime(2019, 4, 22, 19, 41, 00, tzinfo=pytz.UTC)
    )
    timelog4.save()
    # 2.05 2 hours
    timelog6 = TimeLog(
        user=susanna,
        task=task6,
        start_time=datetime(2019, 5, 2, 18, 21, 00, tzinfo=pytz.UTC),
        finish_time=datetime(2019, 5, 2, 20, 49, 00, tzinfo=pytz.UTC)
    )
    timelog6.save()


if __name__ == '__main__':
    run()

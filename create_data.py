from project_manager.models import *
from user_manager.models import *
from datetime import datetime, timedelta


temur = User.objects.get(name="Temur Kholmatov")
danil = User.objects.get(name="Danil Kalinin")
rishat = User.objects.get(name="Rishat Maksudov")
susanna = User.objects.get(name="Susanna Gimaeva")
elena = User.objects.get(name="Elena Patrusheva")


def run():
    project = Project.objects.get(title="Time Tracking System")

    TimeLog.objects.filter(task__project=project).delete()
    Task.objects.filter(project=project).delete()

    task1 = Task(
        title='Statistics Page',
        description='As a developer, I want to use the Dash Plotly framework so that I can create beautiful graphs with statistics.',
        status='done',
        project=project
    )
    task1.save()

    task2 = Task(
        title='Change Instructors',
        description='Add our instructor to the projects',
        status='done',
        project=project
    )
    task2.save()

    task3 = Task(
        title='Fix the add/delete students functionality',
        description='As an instructor, I want to have special buttons so that I can add or delete students to/from a project.',
        status='done',
        project=project
    )
    task3.save()

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

    timelog1 = TimeLog(
        user=rishat,
        task=task1,
        # start_time=datetime(),
        # finish_time=datetime()
    )
    timelog1.save()

    timelog2 = TimeLog(
        user=temur,
        task=task2,
        # start_time=datetime(),
        # finish_time=datetime()
    )
    timelog2.save()

    timelog3 = TimeLog(
        user=danil,
        task=task3,
        # start_time=datetime(),
        # finish_time=datetime()
    )
    timelog3.save()

    timelog4 = TimeLog(
        user=temur,
        task=task4,
        # start_time=datetime(),
        # finish_time=datetime()
    )
    timelog4.save()

    timelog6 = TimeLog(
        user=susanna,
        task=task6,
        # start_time=datetime(),
        # finish_time=datetime()
    )
    timelog6.save()


if __name__ == '__main__':
    run()

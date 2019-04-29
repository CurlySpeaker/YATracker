from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .models import Project, Task, TimeLog
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from user_manager.models import Student
from project_manager.forms import UpdateProjectForm, AddTaskForm
import plotly.offline as opy
import plotly.graph_objs as go

User = get_user_model()


def require_authorized(function):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return function(request, *args, **kwargs)

    return wrapper


@require_authorized
def index(request):
    user = User.objects.get(pk=request.user.id)

    projects = Project.objects.filter(
        Q(students__pk=user.pk) |
        Q(instructor__pk=user.pk)
    ).distinct()
    return render(request, 'project_manager/dashboard.html',
                  {'projects': projects, 'user': user})


@require_authorized
def project_view(request, id):
    user = User.objects.get(pk=request.user.id)
    project = Project.objects.get(pk=id)
    if not (project.students.filter(pk=user.id).exists() or project.instructor.id == user.id):
        return HttpResponseRedirect(reverse('dashboard'))

    if request.method == 'POST':
        form = AddTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            info = form.cleaned_data['info']
            if title:
                task = Task(title=title, description=info, status='todo', project=project)
                task.save()
            else:
                form.add_error(None, "The title is empty")
            return render(request, 'project_manager/project_page.html', {'project': project, 'user': user, 'form': form})
    else:
        form = AddTaskForm()
    return render(request, 'project_manager/project_page.html', {'project': project, 'user': user, 'form': form})


@require_authorized
def to_progress(request, id):
    try:
        task = Task.objects.get(id=id)
    except ObjectDoesNotExist:
        raise Exception('No such task')
    try:
        user = User.objects.get(pk=request.user.id)
    except ObjectDoesNotExist:
        raise Exception('No such user')
    try:
        log = TimeLog.objects.get(user=user, task=task, is_active=True)
        log.finish_time = datetime.now()
    except ObjectDoesNotExist:
        log = TimeLog(user=user, task=task)
        log.start_time = datetime.now()
    log.save()
    project = task.project
    return render(request, 'project_manager/project_page.html', {'project': project, 'user': user})


@require_authorized
def start_task(request, id):
    try:
        task = Task.objects.get(id=id)
    except ObjectDoesNotExist:
        raise Exception('No such task')
    try:
        user = User.objects.get(pk=request.user.id)
    except ObjectDoesNotExist:
        raise Exception('No such user')
    log = TimeLog(user=user, task=task)
    log.start_time = datetime.now()
    log.is_active = True
    log.save()
    task.status = "prog"
    task.save()
    project = task.project
    return render(request, 'project_manager/project_page.html', {'project': project, 'user': user})


@require_authorized
def pause_task(request, id):
    task = Task.objects.get(id=id)
    user = User.objects.get(pk=request.user.id)
    log = TimeLog.objects.get(user=user, task=task, is_active=True)
    log.finish_time = datetime.now()
    log.is_active = False
    log.save()
    task.status = "paus"
    task.save()
    project = task.project
    return render(request, 'project_manager/project_page.html', {'project': project, 'user': user})


@require_authorized
def to_done(request, id):
    try:
        task = Task.objects.get(id=id)
    except ObjectDoesNotExist:
        raise Exception('No such task')
    try:
        user = User.objects.get(pk=request.user.id)
    except ObjectDoesNotExist:
        raise Exception('No such user')
    try:
        log = TimeLog.objects.get(user=user, task=task, is_active=True)
        log.finish_time = datetime.now()
        log.is_active = False
        log.save()
    except ObjectDoesNotExist:
        pass

    task.status = "done"
    task.save()
    project = task.project
    return render(request, 'project_manager/project_page.html', {'project': project, 'user': user})


# modifications only to test frontend (modify_project)
@require_authorized
def modify_project_view(request, id):
    user = User.objects.get(pk=request.user.id)

    project = Project.objects.get(pk=id)
    participants = project.students.all()

    non_participants = Student.objects.exclude(projects=project)
    if request.method == 'POST':
        form = UpdateProjectForm(request.POST)

        team_ids = list(map(int, request.POST.getlist('team')))
        new_students = list(map(int, request.POST.getlist('to_add')))

        if form.is_valid():
            removals = []
            for student in project.students.all():
                if student.id not in team_ids:
                    removals.append(student)
            for removal in removals:
                project.students.remove(removal)

            for student_id in new_students:
                project.students.add(Student.objects.get(id=student_id))

            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            if title:
                project.title = title
                project.description = description
                project.save()
            else:
                form.add_error(None, "The title is empty")
            return render(request, 'project_manager/project_page.html', {'project': project, 'user': user})
    else:
        form = UpdateProjectForm()
    if project.students.filter(pk=user.id).exists() or project.instructor.id == user.id:
        return render(request, 'project_manager/modify_project.html', {
            'project': project,
            'participants': participants,
            'non_participants': non_participants,
            'form': form
        })


@require_authorized
def statistics_view(request, id):
    project = Project.objects.get(pk=id)
    tasks = Task.objects.filter(project=project)
    if tasks is None:
        context = {'no_data': True, 'graph': None, 'graph2': None, 'graph3': None, 'project': project}
        return render(request, 'project_manager/project_stats.html', context)
    logs = TimeLog.objects.filter(task__id__in=tasks.all())

    in_progress = 0
    todo = 0
    done = 0
    for task in tasks:
        if task.status == 'todo':
            todo += 1
        elif task.status == 'done':
            done += 1
    in_progress = len(tasks) - todo - done

    # --------------------------------------------first  graph----------------------------------------------------------

    x = ['TO DO', 'In progress', 'DONE']
    y = [todo, in_progress, done]
    trace1 = go.Bar(
        x=x, y=y,
        # text=['27% market share', '24% market share', '19% market share'],
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity=0.6
    )

    layout = go.Layout(title="Status stats", xaxis={'title': 'Status'}, yaxis={'title': 'Amount'})
    figure = go.Figure(data=[trace1], layout=layout)

    div = opy.plot(figure, auto_open=False, output_type='div')

    # --------------------------------------------second graph----------------------------------------------------------

    x = []
    y = []

    for log in logs:
        days = (log.finish_time.date()-log.start_time.date()).days - 1
        if log.start_time.date() not in x:
            x.append(log.start_time.date())
            y.append(0)
        for i in range(days):
            tmp_date = log.start_time.date() + timedelta(days=i)
            if tmp_date not in x:
                x.append(tmp_date)
                y.append(0)
        if log.finish_time.date() not in x:
            x.append(log.finish_time.date())
            y.append(0)

    for log in logs:
        days = (log.finish_time.date() - log.start_time.date()).days - 1
        # print(days)
        if days == 0:
            difference = (log.start_time.date() + timedelta(days=1) - log.start_time).total_seconds()
            ind = x.index(log.start_time.date())
            y[ind] += difference

            difference = (log.finish_time - log.finish_time.date()).total_seconds()
            ind = x.index(log.finish_time.date())
            y[ind] += difference
        elif days > 0:
            difference = (log.start_time.date() + timedelta(days=1) - log.start_time).total_seconds()
            ind = x.index(log.start_time.date())
            y[ind] += difference

            for i in range(days):
                difference = (log.start_time.date() + timedelta(days=1 + i) - log.start_time + timedelta(days=i)).total_seconds()
                ind = x.index(log.start_time.date() + timedelta(days=i))
                y[ind] += difference

            difference = (log.finish_time - log.finish_time.date()).total_seconds()
            ind = x.index(log.finish_time.date())
            y[ind] += difference
        else:
            difference = (log.finish_time - log.start_time).total_seconds()
            ind = x.index(log.start_time.date())
            y[ind] += difference

    for i in range(len(x) - 1):
        for j in range(i):
            if x[j] > x[j + 1]:
                temp = x[i]
                x[i] = x[i + 1]
                x[i + 1] = temp
                temp = y[i]
                y[i] = y[i + 1]
                y[i + 1] = temp

    trace2 = go.Bar(x=x, y=y)

    layout2 = go.Layout(title="Dates stats", xaxis={'title': 'dates'}, yaxis={'title': 'time (seconds)'})
    figure2 = go.Figure(data=[trace2], layout=layout2)
    div2 = opy.plot(figure2, auto_open=False, output_type='div')

    for log in logs:
        print(log.start_time,  " ", log.finish_time)

    # ---------------------------------------------third graph----------------------------------------------------------

    x_t = []
    y = []

    for task in tasks:
        x_t.append(task)
        y.append(0)

    for log in logs:
        ind = x_t.index(log.task)
        difference = (log.finish_time - log.start_time).total_seconds()
        y[ind] += difference
    x = []
    for i in x_t:
        x.append(i.title[:10])

    trace3 = go.Bar(x=x, y=y)

    layout3 = go.Layout(title="Tasks stats", xaxis={'title': 'tasks'}, yaxis={'title': 'time (seconds)'})
    figure3 = go.Figure(data=[trace3], layout=layout3)
    div3 = opy.plot(figure3, auto_open=False, output_type='div')

    context = {'graph': div, 'graph2': div2, 'graph3': div3, 'no_data': False, 'project': project}

    return render(request, 'project_manager/project_stats.html', context)

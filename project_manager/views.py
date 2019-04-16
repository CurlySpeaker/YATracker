from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .models import Project, Task, TimeLog
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from datetime import datetime
from django.contrib.auth import get_user_model
from user_manager.models import Student
from project_manager.forms import UpdateProjectForm, AddTaskForm

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

        if form.is_valid():
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

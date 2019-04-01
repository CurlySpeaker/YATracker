from django.db.models import Q
from .models import Project, Task, TimeLog, Student, User
from django.shortcuts import render
from django.urls import reverse
from django.http import (
    HttpResponseRedirect,
    HttpResponse,
)
from datetime import datetime

from django.contrib.auth import get_user_model

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
    if project.students.filter(pk=user.id).exists() or project.instructor.id == user.id:
        return render(request, 'project_manager/project_page.html', {'project': project})
    else:
        return HttpResponseRedirect(reverse('dashboard'))


@require_authorized
def to_progress(request, task_id):
    task = Task.objects.get(id=task_id)
    user = User.objects.get(pk=request.user.id)
    log = TimeLog.objects.get(user=user, task=task, is_active=True)
    if log is not None:
        log.finish_time = datetime.now()
    else:
        log = TimeLog(user=user, task=task)
    log.save()
    project = task.project
    return render(request, 'project_manager/project_page.html', {'project': project})


@require_authorized
def start_task(request, task_id):
    task = Task.objects.get(id=task_id)
    user = User.objects.get(pk=request.user.id)
    log = TimeLog.objects.get(user=user, task=task, is_active=True)
    if log is None:
        log = TimeLog(user=user, task=task)
    log.start_time = datetime.now()
    log.is_active = True
    log.save()
    project = task.project
    return render(request, 'project_manager/project_page.html', {'project': project})


@require_authorized
def pause_task(request, task_id):
    task = Task.objects.get(id=task_id)
    user = User.objects.get(pk=request.user.id)
    log = TimeLog.objects.get(user=user, task=task, is_active=True)
    log.finish_time = datetime.now()
    log.is_active = False
    log.save()
    project = task.project
    return render(request, 'project_manager/project_page.html', {'project': project})


@require_authorized
def to_done(request, task_id):
    task = Task.objects.get(id=task_id)
    user = User.objects.get(pk=request.user.id)
    log = TimeLog.objects.get(user=user, task=task, is_active=True)
    if log is not None:
        log.finish_time = datetime.now()
        log.is_active = False
        log.save()
    project = task.project
    return render(request, 'project_manager/project_page.html', {'project': project})


# modifications only to test frontend
@require_authorized
def modify_project_view(request, id):
    user = User.objects.get(pk=request.user.id)
    students = Student.objects.all()

    project = Project.objects.get(pk=id)
    participants = project.students.all()

    non_participants = Student.objects.exclude(projects=project)
    if project.students.filter(pk=user.id).exists() or project.instructor.id == user.id:
        return render(request, 'project_manager/modify_project.html', {
            'project': project,
            'participants': participants,
            'non_participants': non_participants
        })

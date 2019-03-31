from django.db import models
from django.shortcuts import reverse

from user_manager.models import (
    Student,
    Instructor,
)
from .status import STATUS

from django.contrib.auth import get_user_model
User = get_user_model()


class Project(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    students = models.ManyToManyField(Student, related_name='projects')
    instructor = models.ForeignKey(
        Instructor,
        related_name='projects',
        on_delete=models.SET_NULL,
        null=True,
    )

    def get_absolute_url(self):
        return reverse('project', kwargs={'id': self.id})

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    status = models.CharField(max_length=4, choices=STATUS)
    members = models.ManyToManyField(Student, related_name='tasks')
    project = models.ForeignKey(
        Project,
        related_name='tasks',
        on_delete=models.CASCADE,
    )


class TimeLog(models.Model):
    user = models.ForeignKey(
        Student,
        related_name='logs',
        on_delete=models.CASCADE,
    )
    task = models.ForeignKey(
        Task,
        related_name='logs',
        on_delete=models.CASCADE
    )
    is_active = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True, blank=True)
    finish_time = models.DateTimeField(null=True, blank=True)

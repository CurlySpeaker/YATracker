from django.contrib import admin

from .models import (
        Project, Task, TimeLog
)

admin.site.register([
    Project, Task, TimeLog
])

from django.urls import path
from project_manager import views as pm_view

urlpatterns = [
    path('', pm_view.index, name='dashboard'),
    path('project/<int:id>', pm_view.project_view, name='project'),
    path('task_to_started/<int:id>', pm_view.start_task, name='task_to_started'),
    path('task_to_done/<int:id>', pm_view.to_done, name='task_to_done'),
    path('task_to_paused/<int:id>', pm_view.pause_task, name='task_to_paused'),
    path('project/modify_project/<int:id>', pm_view.modify_project_view, name='modify_project'),
    path('project/statistics/<int:id>', pm_view.statistics_view, name='stats_project'),
]

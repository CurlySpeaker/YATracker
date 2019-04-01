from django.urls import path
from project_manager import views as pm_view

urlpatterns = [
    path('', pm_view.index, name='dashboard'),
    path('project/<int:id>', pm_view.project_view, name='project'),
    path('task_to_progress/<int:id>', pm_view.to_progress, name='task_to_progress')
]

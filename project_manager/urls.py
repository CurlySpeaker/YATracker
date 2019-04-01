from django.urls import path
from project_manager import views as pm_view

urlpatterns = [
    path('', pm_view.index, name='dashboard'),
    path('project/<int:id>', pm_view.project_view, name='project'),
    path('project/modify_project/<int:id>', pm_view.modify_project_view, name='modify_project'),
]

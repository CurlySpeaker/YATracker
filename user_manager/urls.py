from django.urls import path
from user_manager import views

urlpatterns = [
    path('', views.personal, name='personal'),
    path('change_password/', views.change_password, name='change_password')
]

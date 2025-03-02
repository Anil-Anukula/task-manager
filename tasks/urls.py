from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),  # Registration URL
    path('login/', views.custom_login_view , name='login'),
    path('logout/', views.custom_logout_view , name='logout'),
    path('', views.home, name='home'),
    path('create/', views.task_create, name='task_create'),
    path('update/<int:task_id>/', views.task_update, name='task_update'),
    path('delete/<int:task_id>/', views.task_delete, name='task_delete'),
    path('task/<int:task_id>/toggle/', views.toggle_task_completion, name='toggle_task'),
]
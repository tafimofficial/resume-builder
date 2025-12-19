from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_resume, name='create_resume'),
    path('resume/<int:pk>/', views.view_resume, name='view_resume'),
    path('resume/<int:pk>/edit/', views.edit_resume, name='edit_resume'),
    path('resume/<int:pk>/export/', views.export_resume, name='export_resume'),
    path('templates/', views.template_gallery, name='template_gallery'),
    path('templates/demo/<str:template_name>/', views.demo_template_view, name='demo_template'),
    # Auth Views
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register, name='register'),
]

from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', login_required(views.index), name='index'),
]

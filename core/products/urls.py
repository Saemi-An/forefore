from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cookies/<str:category>', login_required(views.cookies), name='cookies'),
    path('cookies/change-sales-status/', login_required(views.change_cookies_sale), name='change_cookies_sale'),
    path(
        'cookies/<int:category>/<str:action>/<int:idx>',
        login_required(views.change_cookies_index),
        name='change_cookies_index'
    ),
    path('cookies/pickups/add/', login_required(views.cookies_pickups_add), name='cookies_pickups_add'),
    path('cookies/view/<int:pk>', login_required(views.cookies_view), name='cookies_view'),
    path('cookies/add/<int:pk>', login_required(views.cookies_add), name='cookies_add'),
    path('cookies/delete/<int:pk>/', login_required(views.cookies_delete), name='cookies_delete'),
    path('cookies-products/', login_required(views.cookies_products), name='cookies_products'),
    path('cookies-products/add/', login_required(views.cookies_products_add), name='cookies_products_add'),
    path('cookies-products/view/<int:pk>', login_required(views.cookies_products_view), name='cookies_products_view'),
    path('cookies-products/edit/<int:pk>', login_required(views.cookies_products_edit), name='cookies_products_edit'),
    path(
        'cookies-products/delete/<int:pk>',
        login_required(views.cookies_products_delete),
        name='cookies_products_delete'
    ),
    path('cookies-times/', login_required(views.cookies_times), name='cookies_times'),
    path('cookies-times/view/<int:pk>', login_required(views.cookies_times_view), name='cookies_times_view'),
    path('cookies-times/add/', login_required(views.cookies_times_add), name='cookies_times_add'),
    path('cookies-times/edit/<int:pk>', login_required(views.cookies_times_edit), name='cookies_times_edit'),
    path('cookies-times/delete/<int:pk>', login_required(views.cookies_times_delete), name='cookies_times_delete'),
]

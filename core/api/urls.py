from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path('', views.get_routes),
    path('get-token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('get-refresh-token', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('cookie/<int:pk>/', views.get_cookie),
]

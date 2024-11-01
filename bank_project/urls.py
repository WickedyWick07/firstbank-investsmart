"""
URL configuration for bank_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.http import JsonResponse
from users import views  # Import views from your app

import logging

logger = logging.getLogger(__name__)


def test_view(request):
    return JsonResponse({"message": "Backend API is working!"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', views.register, name='register'),
    path('api/login/', views.login, name='login'),
    path('api/current_user/', views.current_user, name='current_user'),   
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('test/', test_view),  # Add this test endpoint

   

]


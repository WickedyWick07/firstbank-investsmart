# bank_project/urls.py

from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.http import JsonResponse
from users import views as user_views
from accounts import views as account_views

def test_view(request):
    return JsonResponse({"message": "Backend API is working!"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', test_view),
    
    # User URLs
    path('api/register/', user_views.register, name='register'),
    path('api/login/', user_views.login, name='login'),
    path('api/current-user/', user_views.current_user, name='current_user'),
    
    # Token URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Card URLs
    path('api/cards/', account_views.card_list, name='card-list'),
    path('api/card-creation/', account_views.card_list, name='card-creation'),
    path('api/cards/<int:id>/', account_views.card_detail, name='card-detail'),
    path('api/cards/<int:pk>/toggle-active/', account_views.toggle_card_active, name='card-toggle'),
    path('api/cards/<int:pk>/balance/', account_views.card_balance, name='card-balance'),
    
    # Transaction URLs
    path('api/deposit/', account_views.deposit, name='deposit'),
    path('api/withdraw/', account_views.withdraw, name='withdraw'),
    path('api/transactions/history/', account_views.transaction_history, name='transaction-history'),
    
    # Booking URL
    path('api/booking/', account_views.create_booking, name='create-booking'),
]
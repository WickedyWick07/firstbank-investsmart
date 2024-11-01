from django.urls import path
from . import views 
from .views import deposit, withdraw, transaction_history, create_booking

urlpatterns = [
    path('cards/', views.card_list, name='card-list'),
    path('card-creation/', views.card_list, name='card-creation'),
    path('cards/<int:id>/', views.card_detail, name='card-detail'),
    path('cards/<int:pk>/toogle-active/', views.toggle_card_active, name='card-toggle'),
    path('cards/<int:pk>/balance/', views.card_balance, name='card-balance'),
    path('deposit/', deposit, name='deposit'),
    path('withdraw/', withdraw, name='withdraw'),
    path('transactions/history/', transaction_history, name='transaction-history'),
    path('booking/', create_booking, name='create-booking'),
]

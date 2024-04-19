from django.urls import path, include
from .views import *

app_name = 'account'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    path('edit/', profile_edit, name='edit'),
    path('api/create/', UserCreateView.as_view(), name='create'),
    path('token/', TokenCreateView.as_view(), name='token'),
    path('me/', UserView.as_view(), name='me'),
    path('user-orders/<str:user_id>/', UserOrders.as_view(), name='user_orders'),
    path('user-orders-100/<str:user_id>/', UserOrdersRemind.as_view(), name='user_orders_100'),
]
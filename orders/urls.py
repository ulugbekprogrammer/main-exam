from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('created/', views.created, name='created'),
    path('history/', views.history, name='history'),
    path('api/orderitemview/', views.OrderItemView.as_view(), name='order_item'),
    path('api/orderview/', views.OrderView.as_view(), name='order'),
    path('api/orderitemtotal/', views.OrderItemTotal.as_view(), name='order_item_total'),
]
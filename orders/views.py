from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem
from .order import order_created
from django.contrib.auth.decorators import login_required

from .serializers import OrderItemSerializer, OrderSerializer
from rest_framework import generics, authentication, permissions
from rest_framework.response import Response
from django.db.models import Sum

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                new_order = OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'], profile=request.user.profile)
                new_order.save()
            cart.clear()
            order_created.delay(order.id)
            return redirect('created')
    else:
        form = OrderCreateForm()    

    return render(request, 'order/create.html', {'form': form, 'cart':cart})        

@login_required
def history(request):
    orders = Order.objects.filter(items__profile=request.user.profile).order_by('-id').distinct('id')
    return render(request, 'history.html', {'orders': orders})

def created(request):
    return render(request, 'order/created.html', {})

class OrderView(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class OrderItemView(generics.ListAPIView):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class OrderItemTotal(generics.ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        total_cost = OrderItem.objects.all().aggregate(total_cost=Sum('price'))['total_cost']
        return Response({"total_cost": total_cost})  
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UserEditForm
from .models import Profile

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .serializers import UserSerializer, TokenSerializer, UserOrderSerializer
from orders.models import OrderItem
from rest_framework.response import Response
from django.db.models import Sum

@login_required
def profile_edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
            return redirect('account:edit')
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, 'account/edit.html', {'user_form': user_form})      


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return redirect('account:login')
    else:
        form = RegisterForm()
    return render(request, 'account/register.html', {'form':form})

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

class TokenCreateView(ObtainAuthToken):
    serializer_class = TokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserView(generics.RetrieveUpdateDestroyAPIView): 
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class UserOrders(generics.ListAPIView):
    serializer_class = UserOrderSerializer
    queryset = OrderItem.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return OrderItem.objects.filter(profile__user_id=user_id)
    

class UserOrdersRemind(generics.ListAPIView):
    serializer_class = UserOrderSerializer
    queryset = OrderItem.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, user_id, *args, **kwargs):
        total_cost = OrderItem.objects.filter(profile__user_id=user_id).aggregate(total_cost=Sum('price'))['total_cost']
        if total_cost is None:
            total_cost = 0
        more_than_100_dollars = total_cost > 100
        return Response({"more_than_100_$": more_than_100_dollars})


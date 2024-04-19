from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .forms import CartAddProductForm
from .cart import Cart
from django.views.decorators.http import require_POST

@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data

        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])

    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)

    return redirect('cart:cart_detail')

def cart(request):
    cart = Cart(request)
    return render(request, 'detail.html', {'cart': cart})
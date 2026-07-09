from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Cart, CartItem

@login_required(login_url='accounts:login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # User ki active cart dhoondein ya nayi banayein
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check karein ke product pehle se cart mein hai ya nahi
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart, 
        product=product,
        defaults={'price': product.price}
    )
    
    if not item_created:
        # Agar pehle se hai to quantity barha dein
        cart_item.quantity += 1
        cart_item.save()
        
    return redirect('cart:cart_detail')


@login_required(login_url='accounts:login')
def cart_detail(request):
    # User ki cart fetch karein
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Cart ke saare items nikalwain
    cart_items = cart.items.all()
    
    # Total price calculate karein
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price
    })

@login_required(login_url='accounts:login')
def remove_from_cart(request, item_id):
    # Cart item ko direct ID se dhoond kar delete karenge
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart:cart_detail')


@login_required(login_url='accounts:login')
def decrease_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        # Agar quantity 1 ho aur user minus dabaye, to item cart se remove ho jaye
        cart_item.delete()
        
    return redirect('cart:cart_detail')
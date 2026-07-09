
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from .models import OrderItem, Order
from .forms import OrderCreateForm
from django.contrib import messages

@login_required(login_url='accounts:login')
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    
    # Agar cart khali ho to checkout nahi karne dena
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty!")
        return redirect('cart:cart_detail')
        
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = total_price
            order.save()
            
            # Cart Items ko Order Items mein convert karna
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )
                # Product ka stock kam karna
                product = item.product
                product.stock -= item.quantity
                product.save()
                
            # Order complete hone ke baad Cart khali karna
            cart_items.delete()
            
            return render(request, 'orders/order_success.html', {'order': order})
    else:
        form = OrderCreateForm()
        
    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price
    })


@login_required(login_url='accounts:login')
def order_history(request):
    # User ke saare orders fetch ho rahe hain (latest first)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})
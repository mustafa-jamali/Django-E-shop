from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Product,Review
from django.contrib import messages

def product_detail(request, id):
    # Agar slug valid nahi hoga to yeh auto 404 error page dikhaye ga
    product = get_object_or_404(Product, id=id)
    return render(request, 'products/product_detail.html', {'product': product})

@login_required(login_url='accounts:login')
def add_review(request, id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=id)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if rating and comment:
            Review.objects.create(
                product=product,
                user=request.user,
                rating=int(rating),
                comment=comment
            )
            messages.success(request, "Your review has been added successfully!")
        else:
            messages.error(request, "Please provide both rating and comment.")
            
    return redirect('products:product_detail', id=id)
from django.shortcuts import render
from products.models import Product, Category

def home(request):
    # Base Query: Saare products uthao
    products = Product.objects.all()
    categories = Category.objects.all() # Saari categories sidebar ke liye
    
    # 1. Search Logic
    search_query = request.GET.get('search', '')
    if search_query:
        # Product ke naam ya description mein keyword dhoondo
        products = products.filter(name__icontains=search_query)
        
    # 2. Category Filter Logic
    category_id = request.GET.get('category', '')
    if category_id:
        products = products.filter(category_id=category_id)

    return render(request, 'core/home.html', {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id
    })
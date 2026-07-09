from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['product', 'price', 'quantity']
    readonly_fields = ['product', 'price', 'quantity']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Humne list_display mein 'get_products' ka naya column add kiya hai
    list_display = ['id', 'user', 'first_name', 'last_name', 'get_products', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    list_editable = ['status']
    inlines = [OrderItemInline]

    # Yeh function saare products ke naam nikal kar comma se separate karke list mein dikhaye ga
    def get_products(self, obj):
        return ", ".join([f"{item.product.name} (x{item.quantity})" for item in obj.items.all()])
    
    # Column ka naam admin panel par kya show ho
    get_products.short_description = 'Ordered Products'

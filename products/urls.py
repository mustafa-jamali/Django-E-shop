from django.urls import path
from . import views

app_name = 'products' # Namespace define kiya taake dynamic links ban sakein

urlpatterns = [
   path('<int:id>/', views.product_detail, name='product_detail'),
   path('<int:id>/add-review/', views.add_review, name='add_review'),
]
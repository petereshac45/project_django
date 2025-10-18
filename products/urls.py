from django.urls import path
from django.urls import path
from .views import ProductListView, ProductDetailView, ProductBuyView
app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('buy/<int:pk>/', ProductBuyView.as_view(), name='product_buy'),
]

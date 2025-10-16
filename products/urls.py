from .views import ProductListView,HomeView ,ProductDetailView ,ProductBuyView
from django.urls import path

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('Products/', ProductListView.as_view(), name='product_list'),
     path('Products/buy/<int:pk>/', ProductBuyView.as_view(), name='product_buy'),
    path('Products/<int:pk>/', ProductDetailView.as_view(), name='product_detail')
]
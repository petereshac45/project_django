from .views import ProductListView,HomeView ,ProductDetailView ,ProductBuyView , AboutView , ContactView
from django.urls import path

from products.views import ContactView
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('Products/', ProductListView.as_view(), name='product_list'),
     path('Products/buy/<int:pk>/', ProductBuyView.as_view(), name='product_buy'),
    path('Products/<int:pk>/', ProductDetailView.as_view(), name='product_detail')
]
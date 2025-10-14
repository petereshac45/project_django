from .views import ProductListView,HomeView
from django.urls import path

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('Products/', ProductListView.as_view(), name='product_list'),
]
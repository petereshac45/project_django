from django.shortcuts import render
from .models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView ,TemplateView


class HomeView(TemplateView):
    template_name = 'products/home.html'

class ProductListView(LoginRequiredMixin, ListView):
    queryset = Product.objects.filter(is_available=True)
    model = Product
    template_name ='products/product_list.html'
    context_object_name = 'products'
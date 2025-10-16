from django.shortcuts import render , redirect , HttpResponse
from .models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView ,DetailView ,View
from django.views import View

class HomeView(TemplateView):
    template_name = 'products/home.html'

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    queryset = Product.objects.filter(is_available=True)
    template_name = 'products/product_list.html'
    context_object_name = 'products'

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def post(self, request, *args, **kwargs):
  
        product = self.get_object()
    
        return redirect('product_list')

class ProductBuyView(View):
    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return HttpResponse("Product not found", status=404)

        if product.stock > 0:
            product.stock -= 1
            product.save()
            return redirect('product_list')
        else:
            return HttpResponse("Out of stock", status=400)    
from .views import ProductListView,HomeView ,ProductDetailView ,ProductBuyView , AboutView , ContactView
from django.urls import path
app_name = "products"
from products.views import ContactView

urlpatterns = [
    # /products/
    path("", ProductListView.as_view(), name="product_list"),

    # /products/123/
    path("<int:pk>/", ProductDetailView.as_view(), name="product_detail"),

    # /products/buy/123/
    path("buy/<int:pk>/", ProductBuyView.as_view(), name="product_buy"),
]

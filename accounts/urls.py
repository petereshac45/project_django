from django.urls import path
from .views import RegisterView, ProfileView, custom_login_view 
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("signup/", RegisterView.as_view(), name="signup"),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('login/', custom_login_view, name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
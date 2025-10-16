from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

class RegisterView(View):
    def get(self, request):
        return render(request, "accounts/signup.html")

    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not username or not email or not password1 or not password2:
            messages.error(request, "All fields are required.")
            return redirect("signup")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("signup")

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        messages.success(request, "Account created successfully! You can now log in.")
        return redirect("login")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'


def custom_login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            error = "Invalid credentials, please try again."
    return render(request, 'accounts/login.html', {'error': error})

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

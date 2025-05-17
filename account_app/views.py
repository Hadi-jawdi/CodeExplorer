from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.views import PasswordResetView


from django.conf import settings

class CustomPasswordResetView(PasswordResetView):
    template_name = 'account_app/forgot_password.html'
    email_template_name = 'account_app/password_reset_email.html'
    subject_template_name = 'account_app/password_reset_subject.txt'
    success_url = '/account/password_reset_done/'
    from_email = settings.EMAIL_HOST_USER

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not email or not username or not password:
            messages.error(request, 'Please fill out all fields.')
            return render(request, 'account_app/register.html')
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Your account has been created. You can now log in.')
            return redirect('account_app:login')
        except IntegrityError:
            messages.error(request, 'Username already exists. Please choose a different username.')
            return render(request, 'account_app/register.html')
    else:
        return render(request, 'account_app/register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('rememberMe') == 'on'

        if not email or not password:
            messages.error(request, 'Please enter both email and password.')
            return render(request, 'account_app/login.html')

        users = User.objects.filter(email=email)

        if not users.exists():
            messages.error(request, 'Invalid email or password.')
            return render(request, 'account_app/login.html')

        for user_obj in users:
            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                auth_login(request, user)
                if remember_me:
                    request.session.set_expiry(1209600)  # 2 weeks
                else:
                    request.session.set_expiry(0)  # Browser close
                return redirect('core:home')

        messages.error(request, 'Invalid email or password.')
        return render(request, 'account_app/login.html')

    return render(request, 'account_app/login.html')


from django.contrib.auth import logout

def logout_view(request):
    logout(request)  # This logs out the user
    return redirect('account_app:login')  # Redirect to login page



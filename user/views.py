from datetime import timedelta

from django.contrib import auth
from django.contrib.auth import authenticate
from django.utils import timezone

from user.models import User
from django.shortcuts import render, redirect


def welcome(request):
    if request.user.is_authenticated:
        return redirect('index')

    return render(request, 'welcome.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        user = authenticate(request, username=request.POST['email'], password=request.POST['password'])

        if not user:
            return render(request, 'login.html')
        else:
            auth.login(request, user)
            return redirect('index')

    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('index')


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        user = User.objects.filter(email=request.POST['email'])
        if not user:
            user = User.objects.create_user(request.POST['email'],
                                            request.POST['email'],
                                            request.POST['password'])
            auth.login(request, user)

            user.is_trial_used = True
            user.sub_date = timezone.now() + timedelta(days=30)
            user.save()
            return redirect('index')
        else:
            user = authenticate(request, username=request.POST['email'], password=request.POST['password'])
            if user:
                auth.login(request, user)
                return redirect('index')

    return render(request, 'sign_up.html')


def profile(request):
    if not request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        user = request.user

        check = User.objects.filter(email=request.POST.get('email'))
        if check:
            return redirect('profile')

        user.email = request.POST.get('email')
        user.username = request.POST.get('email')
        user.save()

        if request.POST.get('password'):
            user.set_password(request.POST.get('password'))
            user.save()
            auth.login(request, user)
        return redirect('profile')

    return render(request, 'profile.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

import operator
import json
from .forms import RegistrationForm
from .models import User, Teacher, Student

# Create your views here.
def index(request):
    return render(request, "users/index.html")

'''Allowing students and teachers to login'''
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is None:
                messages.error(request, 'Invalid username and/or password.')
            else:
                login(request, user)
                # redirect student and teacher to right pages
                if user.is_teacher:
                    return redirect('teachers:index')
                else:
                    return redirect('students:index')
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {
        'form': form
    })

def logout_view(request):
    logout(request)
    return redirect('users:index')

'''Allowing students and teachers to register'''
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.is_teacher:
                Teacher.objects.create(user=user)
                # redirect teacher to right place
                return redirect('teachers:index')
            else:
                Student.objects.create(user=user)
                return redirect('students:index')
    else:
        form = RegistrationForm()
    return render(request, "users/register.html", {
        'form': form
    })

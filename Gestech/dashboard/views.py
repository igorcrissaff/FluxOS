import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404

def dashboard(request):
    return render(request, 'dashboard.html')

def login(request):
    return render(request, 'login.html')

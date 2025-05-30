from django.shortcuts import render


def index(request):
    return render(request, 'products/index.html')


def login(request):
    return render(request, 'products/login.html')

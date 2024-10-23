from django.shortcuts import render

def home(request):
    return render(request, 'Cuenta/home.html')

def registro(request):
    return render(request, 'Cuenta/registro.html')

def login(request):
    return render(request, 'Cuenta/Login.html')



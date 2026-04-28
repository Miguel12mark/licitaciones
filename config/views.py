from django.shortcuts import render, redirect


def login_view(request):
    return render(request, 'login.html')

def home(request):
    if not request.COOKIES.get('logged'):
        return redirect('/login/')
    
    return render(request, 'home.html')

def crear_usuario_view(request):
    return render(request, 'crear_usuario.html')
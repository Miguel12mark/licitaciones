from django.shortcuts import render, redirect


def login_view(request):
    return render(request, 'login.html')

def home(request):
    # 🔒 si no hay cookie → login
    if not request.COOKIES.get('logged'):
        return redirect('/login/')

    return render(request, 'home.html')
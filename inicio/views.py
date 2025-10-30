from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from core.models import Perfil


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None and hasattr(user, "perfil") and user.perfil.rol == "ALUMNO":
            login(request, user)
            return redirect("alumno:dashboard")   # Cambia a la página de inicio de alumno
        messages.error(request, "Usuario o contraseña incorrectos, o no eres alumno.")
    return render(request, "login_alumno.html")

def index(request):
    """
    Página principal: siempre muestra la portada.
    Puedes mostrar el nombre si está autenticado, pero NUNCA redirige por rol.
    """
    contexto = {}
    if request.user.is_authenticated:
        contexto['username'] = request.user.username
    return render(request, 'inicio/index.html', contexto)

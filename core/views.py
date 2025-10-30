# Create your views here.
from django.shortcuts import render, redirect
from .models import *
from .forms import *

# 🔹 Página de inicio
def home(request):
    return render(request, 'core/home.html')

# 🔹 Subir documentos (solo alumnos)
def subir_documentos(request):
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.alumno = request.user.perfil
            documento.save()
            return redirect('home')
    else:
        form = DocumentoForm()
    return render(request, 'core/subir_documentos.html', {'form': form})


# 🔹 Registrar pago
def registrar_pago(request):
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.alumno = request.user.perfil
            pago.estado = "Completado"
            pago.save()
            return redirect('home')
    else:
        form = PagoForm()
    return render(request, 'core/registrar_pago.html', {'form': form})


# 🔹 Ver progreso
def progreso_alumno(request):
    progreso = Progreso.objects.filter(alumno=request.user.perfil)
    return render(request, 'core/progreso.html', {'progreso': progreso})

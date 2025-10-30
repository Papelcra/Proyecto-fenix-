from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from administracion.models import Pago  # Uso de administracion para pagos
from core.models import Progreso
from administracion.forms import ComprobanteForm
from core.models import Clase

def dashboard(request):
    return render(request, 'alumno/dashboard.html')

@login_required
def pagos(request):
    pagos = Pago.objects.filter(alumno=request.user.perfil).order_by('-fecha_pago')
    return render(request, 'alumno/pagos.html', {'pagos': pagos})

@login_required
def panel_alumno(request):
    pagos = Pago.objects.filter(alumno=request.user.perfil).order_by('-fecha_pago')
    progresos = Progreso.objects.filter(alumno=request.user.perfil).order_by('-fecha')
    return render(request, 'alumno/panel_alumno.html', {'pagos': pagos, 'progresos': progresos})

@login_required
def progreso(request):
    progresos = Progreso.objects.filter(alumno=request.user.perfil).order_by('-fecha')
    return render(request, 'alumno/progreso.html', {'progresos': progresos})

@login_required
def subir_comprobante(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id, alumno=request.user.perfil)
    if request.method == 'POST':
        form = ComprobanteForm(request.POST, request.FILES, instance=pago)
        if form.is_valid():
            pago.comprobante = form.cleaned_data['comprobante']
            pago.estado = 'ENVIADO'
            pago.save()
            return redirect('alumno:pagos')
    else:
        form = ComprobanteForm(instance=pago)
    return render(request, 'alumno/subir_comprobante.html', {'form': form, 'pago': pago})

@login_required
def clases_alumno(request):
    grupos = request.user.perfil.grupos_alumno.all()
    clases = Clase.objects.filter(grupo__in=grupos).order_by('fecha')
    return render(request, 'alumno/clases.html', {'clases': clases})
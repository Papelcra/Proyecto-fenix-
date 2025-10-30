from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from core.models import Grupo, Clase, Perfil, Asistencia, Progreso, Nivel
from django.contrib import messages
from django.contrib.auth import authenticate, login

def login_maestro(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None and hasattr(user, "perfil") and user.perfil.rol == "PROFESOR":
            login(request, user)
            return redirect("maestro:dashboard")
        messages.error(request, "Usuario o contraseña incorrectos, o no eres maestro.")
    return render(request, "login_maestro.html")

@login_required
def dashboard(request):
    try:
        if request.user.perfil.rol != 'PROFESOR':
            return redirect('/')
    except Perfil.DoesNotExist:
        return redirect('/')
    grupos = Grupo.objects.filter(profesor=request.user.perfil)
    return render(request, 'maestro/dashboard.html', {'grupos': grupos})

@login_required
def alumnos_por_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)
    if grupo.profesor != request.user.perfil:
        return redirect('/')
    # Filtrar sólo perfiles de ALUMNO y sin Nones
    alumnos = grupo.alumnos.filter(rol='ALUMNO').exclude(id__isnull=True)
    return render(request, 'maestro/alumnos_por_grupo.html', {'grupo': grupo, 'alumnos': alumnos})

@login_required
def ver_asistencias_alumno(request, alumno_id, grupo_id):
    alumno = get_object_or_404(Perfil, id=alumno_id, rol="ALUMNO")
    grupo = get_object_or_404(Grupo, id=grupo_id)
    asistencias = Asistencia.objects.filter(alumno=alumno).order_by('-fecha')
    clases = Clase.objects.filter(grupo=grupo).order_by('-fecha')

    if request.method == "POST":
        clase_id = request.POST.get("clase_id")
        clase = Clase.objects.get(id=clase_id) if clase_id else None
        presente = True if request.POST.get("presente") == "on" else False
        observacion = request.POST.get("observacion")
        fecha = request.POST.get("fecha")
        from datetime import date
        if not fecha:
            fecha = date.today()
        Asistencia.objects.create(
            alumno=alumno,
            profesor=request.user.perfil,
            fecha=fecha,
            presente=presente,
            observacion=observacion,
            clase=clase  # Relaciona la asistencia con la clase seleccionada
        )
        return redirect('maestro:ver_asistencias_alumno', alumno_id=alumno.id, grupo_id=grupo.id)

    return render(request, 'maestro/asistencias_alumno.html', {
        "alumno": alumno,
        "grupo": grupo,
        "asistencias": asistencias,
        "clases": clases,
        "today": timezone.localdate()  # para prellenar el campo de fecha
    })

@login_required
def reporte_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)
    alumnos = grupo.alumnos.filter(rol='ALUMNO').exclude(id__isnull=True)
    reporte = {}
    ultimas_obs = {}
    for alumno in alumnos:
        asistencias = Asistencia.objects.filter(alumno=alumno, presente=True).count()
        faltas = Asistencia.objects.filter(alumno=alumno, presente=False).count()
        reporte[alumno] = {"asistencias": asistencias, "faltas": faltas}
        ultima = Asistencia.objects.filter(alumno=alumno).order_by('-fecha').first()
        ultimas_obs[alumno.id] = ultima.observacion if (ultima and ultima.observacion) else '-'
    total_registros = sum([s['asistencias'] + s['faltas'] for s in reporte.values()])
    total_asistencias = sum([s['asistencias'] for s in reporte.values()])
    total_faltas = sum([s['faltas'] for s in reporte.values()])
    porcentaje_asistencias = (100 * total_asistencias / total_registros) if total_registros else 0
    porcentaje_faltas = (100 * total_faltas / total_registros) if total_registros else 0
    context = {
        'grupo': grupo,
        'reporte': reporte,
        'total_registros': total_registros,
        'porcentaje_asistencias': porcentaje_asistencias,
        'porcentaje_faltas': porcentaje_faltas,
        'ultimas_obs': ultimas_obs,
    }
    return render(request, 'maestro/reporte_grupo.html', context)

@login_required
def registrar_asistencia_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)
    alumnos = grupo.alumnos.filter(rol='ALUMNO').exclude(id__isnull=True)
    clases = Clase.objects.filter(grupo=grupo).order_by('-fecha')
    fecha_hoy = timezone.localdate()
    if request.method == 'POST':
        clase_id = request.POST.get('clase_id')
        clase = Clase.objects.get(id=clase_id) if clase_id else None
        for alumno in alumnos:
            presente = request.POST.get(f'alumno_{alumno.id}', 'off') == 'on'
            obs = request.POST.get(f'observacion_{alumno.id}', '')
            Asistencia.objects.create(
                alumno=alumno,
                profesor=request.user.perfil,
                fecha=fecha_hoy,
                clase=clase,
                presente=presente,
                observacion=obs,
            )
        messages.success(request, "Asistencia grupal registrada correctamente.")
        return redirect('maestro:dashboard')
    return render(request, 'maestro/registrar_asistencia_grupo.html', {
        'grupo': grupo,
        'alumnos': alumnos,
        'clases': clases,
        'fecha_hoy': fecha_hoy,
    })


@login_required
def editar_progreso_alumno(request, alumno_id, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)
    alumno = get_object_or_404(Perfil, id=alumno_id, rol="ALUMNO")
    niveles = Nivel.objects.all()
    progresos = Progreso.objects.filter(alumno=alumno)
    if request.method == "POST":
        nivel_id = request.POST.get('nivel')
        comentarios = request.POST.get('comentarios')
        completado = request.POST.get('completado') == 'on'
        nivel = get_object_or_404(Nivel, id=nivel_id)
        progreso, created = Progreso.objects.get_or_create(alumno=alumno, nivel=nivel)
        progreso.comentarios = comentarios
        progreso.completado = completado
        progreso.save()
        messages.success(request, "Progreso actualizado correctamente.")
        return redirect('maestro:editar_progreso_alumno', alumno_id=alumno.id, grupo_id=grupo.id)
    return render(request, 'maestro/editar_progreso_alumno.html', {
        'alumno': alumno,
        'grupo': grupo,
        'niveles': niveles,
        'progresos': progresos
    })

from .forms import ClaseForm
from .models import Clase, Grupo

@login_required
def crear_clase(request):
    if request.user.perfil.rol != "PROFESOR":
        return redirect('login')
    grupos = Grupo.objects.filter(profesor=request.user.perfil)
    form = ClaseForm()
    form.fields['grupo'].queryset = grupos
    if request.method == 'POST':
        form = ClaseForm(request.POST)
        form.fields['grupo'].queryset = grupos
        if form.is_valid():
            clase = form.save(commit=False)
            clase.profesor = request.user.perfil
            clase.save()
            messages.success(request, "Clase creada correctamente.")
            return redirect('maestro:listar_clases')
    return render(request, 'maestro/crear_clase.html', {'form': form})

@login_required
def listar_clases(request):
    if request.user.perfil.rol == "PROFESOR":
        clases = Clase.objects.filter(profesor=request.user.perfil)
    elif request.user.perfil.rol == "ADMIN":
        clases = Clase.objects.all()
    else:
        grupos = request.user.perfil.grupos_alumno.all()
        clases = Clase.objects.filter(grupo__in=grupos)
    # Para cada clase, suma presentes y ausentes
    resumen = {}
    for clase in clases:
        asistencias = Asistencia.objects.filter(clase=clase)
        presentes = asistencias.filter(presente=True).count()
        ausentes = asistencias.filter(presente=False).count()
        resumen[clase.id] = {"presentes": presentes, "ausentes": ausentes}
    return render(request, 'maestro/listar_clases.html', {'clases': clases, 'resumen': resumen})

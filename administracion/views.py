from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from core.models import Perfil, Asistencia, Progreso, Nivel, Grupo  # SOLO CORE
from .models import Documento, Pago  # Documentos y pagos sí existen en admin
from django.http import HttpResponse
from .forms import PagoAdminForm 
import csv


def login_admin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None and hasattr(user, "perfil") and user.perfil.rol == "ADMIN":
            login(request, user)
            return redirect("administracion:dashboard_admin")  # Cambia a la página de admin
        messages.error(request, "Usuario o contraseña incorrectos, o no eres administrador.")
    return render(request, "login_admin.html")

def usuario_es_admin(user):
    try:
        return user.perfil.rol == 'ADMIN'
    except Exception:
        return False

@login_required
def dashboard_admin(request):
    if not usuario_es_admin(request.user):
        messages.error(request, "Acceso denegado: solo para administradores.")
        return redirect('login')
    return render(request, 'administracion/dashboard_admin.html', {
        'perfil_usuario': request.user.perfil
    })

@login_required
def panel_usuarios(request):
    if not usuario_es_admin(request.user):
        messages.error(request, "Acceso denegado: solo para administradores.")
        return redirect('login')
    profesores = Perfil.objects.filter(rol='PROFESOR')
    alumnos = Perfil.objects.filter(rol='ALUMNO')
    grupos = Grupo.objects.all()
    context = {
        'perfil_usuario': request.user.perfil,
        'profesores': profesores,
        'alumnos': alumnos,
        'grupos': grupos,
    }
    return render(request, 'administracion/panel_admin.html', context)

@login_required
def crear_usuario(request):
    if not usuario_es_admin(request.user):
        messages.error(request, "Acceso denegado.")
        return redirect('login')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        rol = request.POST.get('rol')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Ese nombre de usuario ya existe.")
            return redirect('administracion:crear_usuario')

        user = User.objects.create_user(username=username, email=email, password=password)
        Perfil.objects.create(user=user, rol=rol)

        messages.success(request, f"Usuario '{username}' creado correctamente como {rol}.")
        return redirect('administracion:panel_usuarios')

    return render(request, 'administracion/crear_usuario.html')

@login_required
def eliminar_usuario(request, perfil_id):
    if not usuario_es_admin(request.user):
        messages.error(request, "Acceso denegado.")
        return redirect('login')
    perfil = get_object_or_404(Perfil, id=perfil_id)
    username = perfil.user.username
    perfil.user.delete()
    messages.success(request, f"Usuario '{username}' eliminado correctamente.")
    return redirect('administracion:panel_usuarios')

@login_required
def asignar_alumnos_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)
    alumnos = Perfil.objects.filter(rol='ALUMNO')
    if request.method == 'POST':
        ids_alumnos = request.POST.getlist('alumnos')
        grupo.alumnos.set(ids_alumnos)
        messages.success(request, "Alumnos asignados correctamente.")
        return redirect('administracion:panel_usuarios')
    return render(request, 'administracion/asignar_alumnos.html', {
        'grupo': grupo,
        'alumnos': alumnos
    })

@login_required
def subir_documento(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)
    alumnos = grupo.alumnos.all()  # Obtener alumnos del grupo
    
    if request.method == 'POST':
        archivo = request.FILES['archivo']
        descripcion = request.POST.get('descripcion', 'Sin descripción')
        tipo = request.POST.get('tipo', 'CEDULA')  # Agregar tipo de documento
        alumno_id = request.POST.get('alumno')  # Obtener alumno seleccionado
        
        if not alumno_id:
            messages.error(request, "Debe seleccionar un alumno.")
            return render(request, 'administracion/subir_documento.html', {
                'grupo': grupo, 
                'alumnos': alumnos
            })
        
        alumno = get_object_or_404(Perfil, id=alumno_id)
        
        Documento.objects.create(
            grupo=grupo, 
            archivo=archivo, 
            descripcion=descripcion,
            tipo=tipo,
            alumno=alumno  # ← ESTO ES LO QUE FALTABA
        )
        
        messages.success(request, "Documento subido correctamente.")
        return redirect('administracion:panel_usuarios')
    
    return render(request, 'administracion/subir_documento.html', {
        'grupo': grupo,
        'alumnos': alumnos
    })

@login_required
def documentos_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)
    documentos = Documento.objects.filter(grupo=grupo)
    alumnos = grupo.alumnos.all()
    if request.method == 'POST':
        for doc in documentos:
            for alumno in alumnos:
                key = f"{doc.id}_{alumno.id}"
                validado = request.POST.get(key) == 'on'
                if validado:
                    doc.alumnos_validado.add(alumno)
                else:
                    doc.alumnos_validado.remove(alumno)
        messages.success(request, "Cambios guardados correctamente.")
        return redirect('administracion:panel_usuarios')
    return render(request, 'administracion/documentos_grupo.html', {
        'grupo': grupo,
        'documentos': documentos,
        'alumnos': alumnos
    })

@login_required
def validar_documentos(request):
    if not request.user.perfil.rol == 'ADMIN':
        return redirect('/')
    grupo_id = request.GET.get('grupo')
    alumno_nombre = request.GET.get('alumno', '').strip().lower()
    documentos = Documento.objects.select_related('alumno', 'grupo').all()

    if grupo_id:
        documentos = documentos.filter(grupo_id=grupo_id)
    if alumno_nombre:
        documentos = documentos.filter(alumno__user__username__icontains=alumno_nombre) | documentos.filter(alumno__user__first_name__icontains=alumno_nombre) | documentos.filter(alumno__user__last_name__icontains=alumno_nombre)

    grupos = Grupo.objects.all()
    alumnos = Perfil.objects.filter(rol='ALUMNO')
    return render(request, 'administracion/validar_documentos.html', {
        'documentos': documentos,
        'grupos': grupos,
        'alumnos': alumnos,
        'grupo_selected': grupo_id or '',
        'alumno_filtro': alumno_nombre or '',
    })


@login_required
def validar_estado_documento(request, doc_id, tipo_doc, accion):
    if not request.user.perfil.rol == 'ADMIN':
        return redirect('/')
    doc = get_object_or_404(Documento, id=doc_id)
    estado = 'VALIDADO' if accion == "validar" else 'RECHAZADO'
    from django.utils import timezone
    doc.fecha_revision = timezone.now()
    doc.estado = estado  # <-- Esta línea actualiza el estado principal visible en tu tabla
    doc.save()
    messages.success(request, f"Documento marcado como {estado.lower()}.")
    return redirect('administracion:validar_documentos')


@login_required
def crear_grupo(request):
    if not usuario_es_admin(request.user):
        messages.error(request, "Acceso denegado.")
        return redirect('login')
    profesores = Perfil.objects.filter(rol='PROFESOR')
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        id_profesor = request.POST.get('profesor')
        profesor = Perfil.objects.get(id=id_profesor) if id_profesor else None
        grupo = Grupo.objects.create(nombre=nombre, descripcion=descripcion, profesor=profesor)
        messages.success(request, f"Grupo '{nombre}' creado correctamente.")
        return redirect('administracion:panel_usuarios')
    return render(request, 'administracion/crear_grupo.html', { 'profesores': profesores })

@login_required
def asignar_profesor_grupo(request, grupo_id):
    if not usuario_es_admin(request.user):
        messages.error(request, "Acceso denegado.")
        return redirect('login')
    grupo = get_object_or_404(Grupo, id=grupo_id)
    profesores = Perfil.objects.filter(rol='PROFESOR')
    if request.method == 'POST':
        id_profesor = request.POST.get('profesor')
        grupo.profesor = Perfil.objects.get(id=id_profesor)
        grupo.save()
        messages.success(request, "Profesor asignado correctamente.")
        return redirect('administracion:panel_usuarios')
    return render(request, 'administracion/asignar_profesor.html', { 'grupo': grupo, 'profesores': profesores })

@login_required
def supervision_reportes(request):
    # Sólo ADMIN puede acceder
    if request.user.perfil.rol != "ADMIN":
        return redirect('/')

    profesores = Perfil.objects.filter(rol="PROFESOR")
    grupos = Grupo.objects.all()

    # Filtros por GET
    grupo_id = request.GET.get('grupo')
    profesor_id = request.GET.get('profesor')
    alumno_nombre = request.GET.get('alumno', '').lower()

    data_grupos = []
    for grupo in grupos:
        if grupo_id and str(grupo.id) != grupo_id:
            continue
        if profesor_id and str(grupo.profesor.id) != profesor_id:
            continue

        grupo_alumnos = grupo.alumnos.filter(rol="ALUMNO")
        alumnos_data = []
        for alumno in grupo_alumnos:
            if alumno_nombre and alumno_nombre not in alumno.user.get_full_name().lower():
                continue

            total_asistencias = Asistencia.objects.filter(alumno=alumno, presente=True).count()
            total_faltas = Asistencia.objects.filter(alumno=alumno, presente=False).count()
            total_registros = total_asistencias + total_faltas

            porcentaje_asistencias = (100 * total_asistencias / total_registros) if total_registros else 0
            porcentaje_faltas = (100 * total_faltas / total_registros) if total_registros else 0

            ultima_asistencia = Asistencia.objects.filter(alumno=alumno).order_by('-fecha').first()
            observacion = ultima_asistencia.observacion if (ultima_asistencia and ultima_asistencia.observacion) else '-'

            progresos = Progreso.objects.filter(alumno=alumno)
            lista_progreso = [{
                "nivel": p.nivel.nombre if p.nivel else "No asignado",
                "comentarios": p.comentarios,
                "completado": p.completado
            } for p in progresos]

            alumnos_data.append({
                "alumno": alumno,
                "porcentaje_asistencias": porcentaje_asistencias,
                "porcentaje_faltas": porcentaje_faltas,
                "observacion": observacion,
                "progresos": lista_progreso,
            })
        if alumnos_data:
            data_grupos.append({
                "grupo": grupo,
                "profesor": grupo.profesor,
                "alumnos": alumnos_data
            })

    # Exportar CSV
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="reporte_supervision.csv"'
        writer = csv.writer(response)
        writer.writerow(["Grupo", "Profesor", "Alumno", "% Asistencia", "% Faltas", "Observación", "Nivel", "Comentarios", "Completado"])
        for grupo in data_grupos:
            for alumno in grupo["alumnos"]:
                for prog in alumno["progresos"]:
                    writer.writerow([
                        grupo["grupo"].nombre,
                        grupo["profesor"].user.get_full_name(),
                        alumno["alumno"].user.get_full_name(),
                        round(alumno["porcentaje_asistencias"], 1),
                        round(alumno["porcentaje_faltas"], 1),
                        alumno["observacion"],
                        prog["nivel"],
                        prog["comentarios"],
                        "Sí" if prog["completado"] else "No",
                    ])
        return response

    context = {
        "profesores": profesores,
        "grupos": data_grupos,
    }
    return render(request, "administracion/supervision_reportes.html", context)

@login_required
def editar_usuario(request, perfil_id):
    if not usuario_es_admin(request.user):
        messages.error(request, "Acceso denegado.")
        return redirect('login')
    perfil = get_object_or_404(Perfil, id=perfil_id)
    user = perfil.user
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        # Puedes agregar más campos para editar...
        user.username = username
        user.email = email
        user.save()
        messages.success(request, "Usuario actualizado correctamente.")
        return redirect('administracion:panel_usuarios')
    return render(request, 'administracion/editar_usuario.html', {'perfil': perfil})

@login_required
def editar_grupo(request, grupo_id):
    if not usuario_es_admin(request.user):
        messages.error(request, "Acceso denegado.")
        return redirect('login')
    grupo = get_object_or_404(Grupo, id=grupo_id)
    if request.method == 'POST':
        grupo.nombre = request.POST.get('nombre')
        grupo.descripcion = request.POST.get('descripcion')
        grupo.save()
        messages.success(request, "Grupo actualizado correctamente.")
        return redirect('administracion:panel_usuarios')
    return render(request, 'administracion/editar_grupo.html', {'grupo': grupo})

@login_required
def eliminar_grupo(request, grupo_id):
    if not usuario_es_admin(request.user):
        messages.error(request, "Acceso denegado.")
        return redirect('login')
    grupo = get_object_or_404(Grupo, id=grupo_id)
    grupo.delete()
    messages.success(request, "Grupo eliminado correctamente.")
    return redirect('administracion:panel_usuarios')

@login_required
def eliminar_documento(request, doc_id):
    if not usuario_es_admin(request.user):
        messages.error(request, "Acceso denegado.")
        return redirect('login')
    doc = get_object_or_404(Documento, id=doc_id)
    doc.delete()
    messages.success(request, "¡Documento eliminado correctamente!")
    return redirect('administracion:validar_documentos')

@login_required
def pagos_admin(request):
    if not usuario_es_admin(request.user):
        messages.error(request, "Acceso denegado: solo administradores.")
        return redirect('login')
    alumno_id = request.GET.get("alumno")
    pagos = Pago.objects.select_related('alumno').all().order_by('-fecha_pago')
    if alumno_id:
        pagos = pagos.filter(alumno__id=alumno_id)
    alumnos = Perfil.objects.filter(rol="ALUMNO")
    return render(request, "administracion/pagos_admin.html", {
        "pagos": pagos,
        "alumnos": alumnos,
        "alumno_id": alumno_id,
    })

@login_required
def crear_pago(request):
    if not usuario_es_admin(request.user):
        messages.error(request, "Acceso denegado.")
        return redirect('login')
    if request.method == 'POST':
        form = PagoAdminForm(request.POST)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.estado = 'PENDIENTE'
            pago.save()
            messages.success(request, "Pago asignado correctamente al alumno.")
            return redirect('administracion:pagos_admin')
    else:
        form = PagoAdminForm()
    return render(request, "administracion/crear_pago.html", {"form": form})

@login_required
def eliminar_pago(request, pago_id):
    if not usuario_es_admin(request.user):
        messages.error(request, "Acceso denegado.")
        return redirect('login')
    pago = get_object_or_404(Pago, id=pago_id)
    pago.delete()
    messages.success(request, "Pago eliminado.")
    return redirect('administracion:pagos_admin')

@login_required
def validar_pago(request, pago_id):
    if not usuario_es_admin(request.user):
        messages.error(request, "Acceso denegado.")
        return redirect('login')
    pago = get_object_or_404(Pago, id=pago_id)
    pago.estado = 'VALIDADO'
    pago.save()
    messages.success(request, "Pago validado correctamente.")
    return redirect('administracion:pagos_admin')

@login_required
def rechazar_pago(request, pago_id):
    if not usuario_es_admin(request.user):
        messages.error(request, "Acceso denegado.")
        return redirect('login')
    pago = get_object_or_404(Pago, id=pago_id)
    pago.estado = 'RECHAZADO'
    pago.save()
    messages.success(request, "Pago rechazado correctamente.")
    return redirect('administracion:pagos_admin')

from core.models import Clase, Grupo, Perfil  # Importa desde core tus modelos de clases y grupos

@login_required
def clases_admin(request):
    if not usuario_es_admin(request.user):
        messages.error(request, "Acceso denegado: solo para administradores.")
        return redirect('login')
    grupos = Grupo.objects.all().select_related('profesor').prefetch_related('alumnos')
    clases = Clase.objects.select_related('grupo', 'profesor').order_by('-fecha')
    profesores = Perfil.objects.filter(rol='PROFESOR')
    return render(request, 'administracion/clases_admin.html', {
        'clases': clases,
        'grupos': grupos,
        'profesores': profesores,
    })

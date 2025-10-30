from django.contrib.auth.models import User
from core.models import Perfil
from maestro.models import Grupo
from alumno.models import Alumno
from administracion.models import Grupo_alumnos
def alumno_to_perfil(alumno):
    username = f'alumno_{alumno.codigo}'
    user, created = User.objects.get_or_create(username=username)
    perfil, created_perf = Perfil.objects.get_or_create(
        user=user,
        defaults={"rol": "ALUMNO"}
    )
    if created:
        user.first_name = alumno.nombre
        user.save()
    return perfil
for grupo_old in Grupo_alumnos.objects.all():
    print("Migrando grupo:", grupo_old.nombre)
    maestro = Perfil.objects.filter(rol='PROFESOR').first()
    if not maestro:
        print('No hay maestro, salta grupo:', grupo_old.nombre)
        continue
    grupo_new, g_created = Grupo.objects.get_or_create(
        nombre=grupo_old.nombre,
        defaults={"descripcion": grupo_old.descripcion, "maestro": maestro}
    )
    grupo_new.maestro = maestro
    perfiles_alumnos = []
    for alumno in grupo_old.alumnos.all():
        perfil = alumno_to_perfil(alumno)
        perfiles_alumnos.append(perfil)
        print(f' - Alumno migrado: {alumno.nombre} como perfil {perfil.user.username}')
    grupo_new.save()
    grupo_new.alumnos.set(perfiles_alumnos)
    grupo_new.save()
    print('Grupo migrado:', grupo_new)
print('Migración terminada')

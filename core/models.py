from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    ROLES = [
        ('ALUMNO', 'Alumno'),
        ('PROFESOR', 'Profesor'),
        ('ADMIN', 'Administrador'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=10, choices=ROLES)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    documento = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.rol}"

class Grupo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    profesor = models.ForeignKey(
        Perfil,
        on_delete=models.SET_NULL,
        limit_choices_to={'rol': 'PROFESOR'},
        related_name='grupos_dirigidos',
        null=True,
        blank=True
    )
    alumnos = models.ManyToManyField(
        Perfil,
        limit_choices_to={'rol': 'ALUMNO'},
        related_name='grupos_alumno',
        blank=True
    )

    def __str__(self):
        profe_str = self.profesor.user.username if self.profesor else "Sin profesor"
        return f"{self.nombre} - {profe_str}"

class Clase(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='clases')
    profesor = models.ForeignKey(Perfil, on_delete=models.CASCADE, limit_choices_to={'rol': 'PROFESOR'})
    fecha = models.DateField()
    descripcion = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.grupo.nombre} - {self.fecha} - {self.descripcion[:35]}"

class Documento(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('VALIDADO', 'Validado'),
        ('RECHAZADO', 'Rechazado'),
    ]
    alumno = models.ForeignKey(
        Perfil,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'ALUMNO'},
        related_name='documentos_core',
    )
    cedula = models.FileField(upload_to='documentos/cedulas/')
    estado_cedula = models.CharField(max_length=10, choices=ESTADOS, default='PENDIENTE')
    eps = models.FileField(upload_to='documentos/eps/')
    estado_eps = models.CharField(max_length=10, choices=ESTADOS, default='PENDIENTE')
    autorizacion = models.FileField(upload_to='documentos/autorizaciones/')
    estado_autorizacion = models.CharField(max_length=10, choices=ESTADOS, default='PENDIENTE')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    fecha_revision = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Documentos de {self.alumno.user.username if self.alumno else 'SIN ALUMNO'}"

class Nivel(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    orden = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nombre

class Membresia(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_dias = models.PositiveIntegerField()
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

class Pago(models.Model):
    alumno = models.ForeignKey(
        Perfil,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'ALUMNO'},
        related_name='pagos_core',
        null=True,
        blank=True
    )
    membresia = models.ForeignKey(Membresia, on_delete=models.SET_NULL, null=True)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, default='Completado')

    def __str__(self):
        return f"Pago de {self.alumno.user.username if self.alumno else 'SIN ALUMNO'} - {self.valor}"

class Clase(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='clases')
    profesor = models.ForeignKey(Perfil, on_delete=models.CASCADE, limit_choices_to={'rol': 'PROFESOR'})
    fecha = models.DateField()
    descripcion = models.CharField(max_length=250)
    # Si quieres marcar tipo/práctica: tipo = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return f"{self.grupo.nombre} - {self.fecha} - {self.descripcion[:35]}"

class Asistencia(models.Model):
    clase = models.ForeignKey(Clase, on_delete=models.SET_NULL, null=True, blank=True)
    profesor = models.ForeignKey(
        Perfil,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'PROFESOR'},
        related_name='asistencias_registradas'
    )
    alumno = models.ForeignKey(
        Perfil,
        on_delete=models.CASCADE,
        related_name='asistencias_recibidas',
        limit_choices_to={'rol': 'ALUMNO'},
        null=True,
        blank=True
    )
    fecha = models.DateField(auto_now_add=True)
    presente = models.BooleanField(default=False)
    observacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Asistencia {self.alumno.user.username if self.alumno else 'SIN ALUMNO'} ({'Presente' if self.presente else 'Ausente'})"

class Progreso(models.Model):
    alumno = models.ForeignKey(
        Perfil,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'ALUMNO'},
        related_name='progresos_core',
        null=True,
        blank=True
    )
    nivel = models.ForeignKey(Nivel, on_delete=models.SET_NULL, null=True)
    comentarios = models.TextField(blank=True, null=True)
    completado = models.BooleanField(default=False)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        if self.nivel and self.alumno:
            return f"{self.alumno.user.username} - {self.nivel.nombre}"
        elif self.alumno:
            return f"{self.alumno.user.username} - Nivel no asignado"
        return "SIN ALUMNO - Nivel no asignado"

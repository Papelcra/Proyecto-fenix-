from django.db import models
from core.models import Perfil, Grupo  # SOLO CORE

class Pago(models.Model):
    ESTADO_CHOICES = (
        ('PENDIENTE', 'Pendiente'),
        ('ENVIADO', 'Comprobante enviado'),
        ('VALIDADO', 'Validado por admin'),
        ('RECHAZADO', 'Rechazado por admin'),
    )
    alumno = models.ForeignKey(Perfil, on_delete=models.CASCADE, limit_choices_to={'rol': 'ALUMNO'}, related_name='pagos_administracion')
    fecha_pago = models.DateField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    estado = models.CharField(max_length=12, choices=ESTADO_CHOICES, default='PENDIENTE')
    comprobante = models.FileField(upload_to='comprobantes/', null=True, blank=True)

    def __str__(self):
        return f"{self.alumno.user.username} - {self.monto} - {self.fecha_pago} - {self.estado}"

class Documento(models.Model):
    alumno = models.ForeignKey(
        Perfil,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'ALUMNO'},
        related_name='documentos_administracion'
    )
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.CharField(max_length=40, choices=(
        ('CEDULA', 'Cédula'),
        ('EPS', 'EPS'),
        ('AUTORIZACION', 'Autorización'),
    ))
    archivo = models.FileField(upload_to='documentos/')
    descripcion = models.TextField(default="Sin descripción")
    estado = models.CharField(max_length=20, choices=(
        ('PENDIENTE', 'Pendiente'),
        ('VALIDADO', 'Validado'),
        ('RECHAZADO', 'Rechazado'),
    ), default='PENDIENTE')
    fecha_revision = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.tipo} - {self.alumno.user.get_full_name()}"

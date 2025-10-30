from django.db import models

# Puedes comentar o eliminar estos si sólo usas Perfil/Grupo/Pago de core
class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)
    curso = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Nota(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    materia = models.CharField(max_length=100)
    nota = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.alumno.nombre} - {self.materia}"

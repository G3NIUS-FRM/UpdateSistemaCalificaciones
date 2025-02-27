from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Cursos(models.Model):
    Curso=models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.Curso
class Materias(models.Model):
    Materia=models.CharField(max_length=100,unique=True)
    cursos = models.ManyToManyField(Cursos)
    def __str__(self):
        return self.Materia
class Profesores(models.Model):
    Profesor=models.OneToOneField(User, on_delete=models.CASCADE)
    Materia=models.ForeignKey(Materias, on_delete=models.CASCADE)
    Cursos=models.ManyToManyField(Cursos)
    def __str__(self):
        return f"{self.Profesor}"
class Estudiantes(models.Model):
    Nombre=models.CharField(max_length=100)
    Curso=models.ForeignKey(Cursos, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.Nombre}"
class Calificaciones(models.Model):
    PERIODO_CHOICES = [
        (1, 'Primer Trimestre'),
        (2, 'Segundo Trimestre'),
        (3, 'Tercer Trimestre'),
    ]
    Estudiante=models.ForeignKey(Estudiantes, on_delete=models.CASCADE)
    Materia=models.ForeignKey(Materias, on_delete=models.CASCADE)

    Calificacion=models.IntegerField()
    Periodo=models.IntegerField(choices=PERIODO_CHOICES)
    fecha_registro=models.DateField(auto_now=True)

    class Meta:
        unique_together=['Estudiante','Materia','Periodo']
        
    def __str__(self):
        return f"{self.Estudiante} - {self.Materia} - {self.Calificacion}"
class Apuntes(models.Model):
    Maestro=models.ForeignKey(Profesores,on_delete=models.CASCADE)
    Estudiante_ref=models.ForeignKey(Estudiantes , on_delete=models.CASCADE)
    Notas=models.TextField()
    FechaDeRegistro=models.DateField(auto_now=True)
    def __str__(self):
        return f"{self.Estudiante_ref} - {self.Maestro} - {self.FechaDeRegistro}"
class Historial(models.Model):
    Maestro=models.ForeignKey(Profesores,on_delete=models.CASCADE)
    Estudiante=models.ForeignKey(Estudiantes,on_delete=models.CASCADE)
    Old=models.IntegerField()
    New=models.IntegerField()
    Cambio=models.CharField(max_length=30, default="Agregar")
    
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Clase de la victima, esta clase representa una entidad en la tabla de base de datos, en este caso la entidad representa la victica que esta haciendo la demanda.
class Victima(models.Model):
  # Atributos que representan a la victima
  nombre = models.CharField(default='Anonimo', max_length=50)
  primerApellido = models.CharField(default='Anonimo', max_length=50)
  segundoApellido = models.CharField(default='Anonimo', max_length=50)
  edad = models.IntegerField(default=0)
  tipoDocumento = models.CharField(default='No tiene', max_length=50)
  numeroDocumento = models.CharField(default='No se sabe', max_length=50)
  ciudadNacimiento = models.CharField(default='No esta definida', max_length=50)
  ciudadRecidencia = models.CharField(default='No esta definida', max_length=50)

# Clase agresor, esta clase representa una entidad en la tabla de base de datos, en este caso esta representando al agresor.
class Agresor(models.Model):
  # Atritutos que representan al agresor
  nombre = models.CharField(default='Anonimo', max_length=50)
  primerApellido = models.CharField(default='Anonimo', max_length=50)
  segundoApellido = models.CharField(default='Anonimo', max_length=50)
  tipoDocumento = models.CharField(default='No se especifica', max_length=50)
  numeroDocumento = models.CharField(default='No se especifica', max_length=50)
  ciudadNacimiento = models.CharField(default='No se especifica', max_length=50)
  ciudadResidencia = models.CharField(default='No se especifica', max_length=50)
  antecedentesPenales = models.TextField(default='No se conocen', max_length=50)

# Clase denuncia, esta clase representa una entidad en la tabla de base de datos, en este caso la entidad representada es la demanda la cual tiene como fin relacionar a la victima como al agresor
class Denuncia(models.Model):
  # Atributos de denuncia
  agresor = models.ForeignKey(Agresor, on_delete=models.CASCADE)
  victima = models.ForeignKey(Victima, on_delete=models.CASCADE)
  gradoDeViolencia = models.IntegerField(default=0)
  fecha = models.DateTimeField(default=None)
  descripcion = models.TextField(default='No hay suficiente informacion para generar una descripcion', max_length=1000)
  prevenciones = models.TextField(default='No estan disponibles', max_length=1000)
  ubicacion = models.CharField(default='No se conoce la ubicacion de la demanda', max_length=50)
  tipoDeDenuncia = models.CharField(default='No se especifica', max_length=20)

  # Metodos de instancia
  def generarPrevenciones(self)->float:
    pass

  def calcularProbabilidadExito(self)->float:
    pass

  def calcularPorcentajeExtioSolucion(self)->float:
    pass

  def analisisSituacion(self)->str:
    pass

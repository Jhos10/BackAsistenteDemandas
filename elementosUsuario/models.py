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

  # Factory metodo

  # Constructor para una persona que cuanta con la informacion de nombre, primer apellido y segundo apellido
  @classmethod
  def constructorSeleniumIdentidadCompleta(cls,nombre,primerApellido,segundoApellido):
    return cls(nombre=nombre,primerApellido=primerApellido,segundoApellido=segundoApellido)

  # Constructor para una persona que cuenta con unicamente el nombre
  @classmethod
  def constructorSeleniumUniNombre(cls,nombre):
    return cls(nombre=nombre)
  
  # Constructor para una persona que cuenta con nombre y primer apellido
  @classmethod
  def constructorSeleniumNombreApellido(cls,nombre,primerApellido):
    return cls(nombre=nombre,primerApellido=primerApellido)
  


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
  entidad = models.BooleanField(default=False)

  # Factory method

  # Constructor
  @classmethod
  def seleniumConstructorEntidad(cls,nombreEntidad):
    return cls(nombre=nombreEntidad,entidad=True)

  @classmethod
  def seleniumConstructorAgresoPersonaUniNombre(cls,nombrePersona):
    return cls(nombre=nombrePersona)

  @classmethod
  def seleniumConstructorAgresorPersonaNombreApellido(cls,nombrePesona,primerApellido):
    return cls(nombre=nombrePesona,primerApellido=primerApellido)

  @classmethod
  def seleniumConstructorAgresorIdentidadCompleta(cls,nombrePersona,primerApellido,segundoApellido):
    return cls(nombre = nombrePersona,primerApellido=primerApellido,segundoApellido=segundoApellido)
  
  

# esta clase representa una entidad en la tabla de base de datos, en este caso la entidad representada es la demanda la cual tiene como fin relacionar a la victima como al agresor
class Denuncia(models.Model):
  # Atributos de denuncia
  titulo = models.CharField(max_length=100,default='No cuenta con titulo')
  agresor = models.ForeignKey(Agresor, on_delete=models.CASCADE)
  victima = models.ForeignKey(Victima, on_delete=models.CASCADE)
  gradoDeViolencia = models.IntegerField(default=0)
  fecha = models.DateTimeField(default=None)
  descripcion = models.TextField(default='No hay suficiente informacion para generar una descripcion', max_length=1000)
  prevenciones = models.TextField(default='No estan disponibles', max_length=1000)
  ubicacion = models.CharField(default='No se conoce la ubicacion de la demanda', max_length=50)
  tipoDeDenuncia = models.CharField(default='No se especifica', max_length=20)

  @classmethod
  def constructorSelenium(cls,agresor,victima,fecha,descripcion,tituloSentencia):
    return cls.objects.create(agresor=agresor,victima=victima,fecha=fecha,descripcion=descripcion,titulo=tituloSentencia)

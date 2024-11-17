# Importar las librerias necesarias
import json
import random
from functools import reduce
from .models import Victima, Agresor, Denuncia
from Scrapy.ScrapingCorteSelenium import scrapyLista
# from .models import *
import pprint as pp

class VictimaRepresentacion:
    def __init__(self,nombre,primerApellido,segundoApellido):
        self.nombre = nombre
        self.primerApellido = primerApellido
        self.segundoApellido = segundoApellido

class VictimaSelenium(VictimaRepresentacion):
    def __init__(self, nombre, primerApellido, segundoApellido):
        super().__init__(nombre, primerApellido, segundoApellido)

    def filtrarPalabrasVictima(self,informacion:list)->list:
        listaDePalabras = ['DE','OFICIO','PROCESADO','OTROS', 'Y','OFICIOS','OTRO','OTRA', 'OTRAS', 'SALA','SEGUIMIENTO',""]
        listaFiltrada = list(filter(lambda x: True if x.upper() not in listaDePalabras else False, informacion))
        if len(listaFiltrada) != 0:
            return listaFiltrada
        else:
            return []

    def ajustarIdentidad(self)->VictimaRepresentacion:
        informacionIdentidadLista = self.nombre.split(" ")
        listaPalabras = self.filtrarPalabrasVictima(informacionIdentidadLista)
        if len(self.nombre) > 7:
            return None
        elif len(listaPalabras) == 1:
            self.nombre = listaPalabras[0]
        elif len(listaPalabras) == 2:
            # print(listaPalabras)
            self.nombre = listaPalabras[0]
            self.primerApellido = listaPalabras[1]
        elif len(listaPalabras) == 3:
            self.nombre = listaPalabras[0]
            self.primerApellido = listaPalabras[1]
            self.segundoApellido = listaPalabras[2]
        elif len(listaPalabras) == 4: 
            self.nombre = listaPalabras[0]
            self.primerApellido = listaPalabras[2]
            self.segundoApellido = listaPalabras[3]
        elif listaPalabras == []:
            return None
        
    @staticmethod
    def generarModeloBaseDatos(victima:VictimaRepresentacion)->Victima:
        return Victima.elegirConstructor(victima)
    
    def guardarRegistroBd(victima:Victima)->None:
        victima.save()

class VictimaScrapy(VictimaRepresentacion):
    def __init__(self, nombre, primerApellido, segundoApellido,edad,tipoDocumento,numeroDocumento, ciudadNacimiento,ciudadRecidencia):
        super().__init__(nombre, primerApellido, segundoApellido)
        self.edad = edad
        self.tipoDocumento = tipoDocumento
        self.numeroDocumento = numeroDocumento
        self.ciudadNacimiento = ciudadNacimiento
        self.ciudadRecidencia = ciudadRecidencia

    def organizarCadena(self,nombre:str)->str:
        lista = nombre.split(':')
        return lista[1]

    def ajustarDatos(self):
        self.nombre = self.organizarCadena(self.nombre)
        self.primerApellido = self.organizarCadena(self.primerApellido)
        self.segundoApellido = self.organizarCadena(self.segundoApellido)
        self.edad = self.organizarCadena(self.edad)
        self.tipoDocumento = self.organizarCadena(self.tipoDocumento)
        self.numeroDocumento = self.organizarCadena(self.numeroDocumento)
        self.ciudadNacimiento = self.organizarCadena(self.ciudadNacimiento)
        self.ciudadRecidencia = self.organizarCadena(self.ciudadRecidencia)

    @staticmethod 
    def generarRegistroDb(victima):
        return Victima.objects.create(nombre = victima.nombre,primerApellido =victima.primerApellido, segundoApellido = victima.segundoApellido,edad = victima.edad, tipoDocumento = victima.tipoDocumento,numeroDocumento = victima.numeroDocumento, ciudadNacimiento = victima.ciudadNacimiento,ciudadRecidencia = victima.ciudadRecidencia)

class AgresorRepresentacion:
    def __init__(self,nombre, primerApellio, segundoApellido):
        self.nombre = nombre
        self.primerApellido = primerApellio
        self.segundoApellido = segundoApellido

class AgresorSelenium(AgresorRepresentacion):
    def __init__(self, nombre, primerApellio, segundoApellido):
        super().__init__(nombre, primerApellio, segundoApellido)
    
    # Determina si se puede determinar el tipo de agresor y tambien su identidad.
    def determinarValidesAgresor(self,lista:list)->bool:
        # Lista de palabras que determinan si es posible validar la identidad de la entidad o la persona.
        listaPalabras = ['y', 'otros']

        # Recorrer la lista de palabras que estan completamente en minuscula.
        for palabra in lista:
            # Condicion para verificar si la palabras es una de las palabras que verifican que no es un usuario que se puede guardar en la base de datos.
            if palabra in listaPalabras:
                # Retorna verdadero, afirmando que el usuario no es valido para guardar en la base de datos.
                return True
        
        # Retorna falso, afirmando que el usuario es valido para ser guardado en la base de datos.
        return False

    def filtrarPalabrasAgresor(self,informacion)->tuple:
        listaMinusculas = list(map(lambda x: x.lower(), informacion))
        verificarValides = self.determinarValidesAgresor(listaMinusculas)
        print(verificarValides)
        if verificarValides == True:
            # El cero representa que no es valido
            return verificarValides,0
        
        listaPalabras = ['tribunal', 'superior', 'judicial','ley','municipio','ministerio','periodico','fundacion', 'fiscalia', 'fondo', 'universidad', 'fonvivienda','consejo', 'juzgado', 'institución', 'sas', 'comisaria', 'eps', 'secretaria','fonvivienda','alcaldia','codigo']

        for palabra in listaMinusculas:
            if palabra in listaPalabras:
                # El uno representa que este usuario es valido para ser guardado como entidad
                return True,1
        
        # El uno representa que este usuario es valido para ser guardado como persona
        return False,1

    def ajustarIdentidad(self,informacion:str)->Agresor:
        informacionIdentidadLista = self.nombre.split(' ')
        tipoAgresor = self.filtrarPalabrasAgresor(informacionIdentidadLista)
        if tipoAgresor[0] == True and tipoAgresor[1] == 1:
            pass
        elif tipoAgresor[0] == False:
            if len(informacion) == 1:
                agresor = Agresor.seleniumConstructorAgresoPersonaUniNombre
                (informacionIdentidadLista[0])
                self.nombre = informacionIdentidadLista[0]
            elif len(informacion) == 2:
                self.nombre = informacionIdentidadLista[0]
                self.primerApellido = informacionIdentidadLista[1]
            elif len(informacion) == 3:
                self.nombre = informacionIdentidadLista[0]
                self.primerApellido = informacionIdentidadLista[1]
                self.segundoApellido = informacionIdentidadLista[2]
            elif len(informacion) == 4:
                self.nombre = informacion[0]
                self.primerApellido = informacion[2]
                self.segundoApellido = informacion[3]
        else:
            self.nombre = None

    @staticmethod
    def registrarAgresor(agresor:AgresorRepresentacion)->Agresor:
        return Agresor.elegirConstructor(agresor)

    @staticmethod
    def guardarRegistroBd(agresor:Agresor)->None:
        agresor.save()
        

class AgresorScrapy(AgresorRepresentacion):
    def __init__(self, nombre, primerApellio, segundoApellido, tipoDocumento,numeroDocumento,ciudadNacimiento,ciudadResidencia,entidad):
        super().__init__(nombre, primerApellio, segundoApellido)
        self.tipoDocumento = tipoDocumento
        self.numeroDocumento = numeroDocumento
        self.ciudadNacimiento = ciudadNacimiento
        self.ciudadResidencia = ciudadResidencia
        self.entidad = entidad

    def organizarCadena(self,nombre:str)->str:
        lista = nombre.split(':')
        return lista[1]
        
    def ajustarDatos(self):
        self.nombre = self.organizarCadena(self.nombre)
        self.primerApellido = self.organizarCadena(self.primerApellido)
        self.segundoApellido = self.organizarCadena(self.segundoApellido)
        self.tipoDocumento = self.organizarCadena(self.tipoDocumento)
        self.numeroDocumento = self.organizarCadena(self.numeroDocumento)
        self.ciudadNacimiento = self.organizarCadena(self.ciudadNacimiento)
        self.ciudadResidencia = self.organizarCadena(self.ciudadResidencia)
        
    @staticmethod
    def generarRegistroDb(agresor):
        return Agresor.objects.create(nombre = agresor.nombre, primerApellido = agresor.primerApellido, segundoApellido = agresor.segundoApellido, tipoDocumento = agresor.tipoDocumento, numeroDocumento = agresor.numeroDocumento, ciudadNacimiento = agresor.ciudadNacimiento, ciudadResidencia = agresor.ciudadResidencia, entidad = agresor.entidad)


    

class DenunciaRepresentacion:
    def __init__(self,titulo, agresor, victima, fecha, descripcion,prevenciones):
        self.titulo = titulo
        self.agresor = agresor
        self.victima = victima
        self.fecha = fecha
        self.descripcion = descripcion
        self.prevenciones = prevenciones

class DenunciaSelenium(DenunciaRepresentacion):
    def __init__(self, titulo, agresor, victima, fecha, descripcion, prevenciones = None):
        super().__init__(titulo, agresor, victima,fecha, descripcion, prevenciones)

    @staticmethod
    def generarRegistroDb(denuncia:DenunciaRepresentacion,victima:VictimaSelenium,agresor:AgresorSelenium)->Denuncia:
        return Denuncia.constructorSelenium(agresor=denuncia.agresor,victima=denuncia.victima,fecha=denuncia.fecha,descripcion=denuncia.descripcion,tituloSentencia=denuncia.titulo)
    
    @staticmethod
    def guardarDenunciaDb(denuncia:Denuncia)->None:
        denuncia.save()

class DenunciaScrapy(DenunciaRepresentacion):

    def __init__(self, titulo = None, agresor = None, victima = None, fecha = None, descripcion = None, prevenciones = None,ubicacion = None,ciudad = None):
        super().__init__(titulo, agresor, victima, fecha, descripcion, prevenciones)
        self.ubicacion = ubicacion
        self.ciudad = ciudad
        
    def organizarCadena(self,nombre:str)->str:
        lista = nombre.split(':')
        return lista[1]



    def agregarDireccion(self)->str:
        direccion = ["Avenida 30 de Agosto No 68 - 125 Barrio Cañaveral",
        "Calle 71 No 26 - 57 Barrio Cuba", 
        "Avenida Las Américas No 53 - 20 Barrio Avenida Sur", 
        "Avenida 30 de Agosto No 42 - 75 Barrio Maraya", 
        "Carrera 8 Bis No 30 B - 49 Barrio Centro", 
        "Avenida 30 de Agosto No 30 - 30 Local 27 Barrio Repuestos", 
        "Carrera 7 No 25 - 18 Barrio Centro", 
        "Carrera 9 No 21 - 03 Barrio Centro", 
        "Carrera 10 No 16 - 60 Barrio C. Cultural Lucy Tejeda", 
        "Avenida Circunvalar No 10 - 26 Barrio Circunvalar", 
        "Calle 16 No 6 - 34 Barrio Centro", 
        "Carrera 15A No 148 - 37 Barrio La Julita", 
        "Carrera 5 No 16 - 63 Barrio San Nicolás", 
        "Calle 69 No 25 - 08 Barrio Cuba", 
        "Carrera 2 No 23 - 29 Barrio San Joaquín", 
        "Carrera 13 No 15 - 35 Barrio El Centro", 
        "Calle 21 No 4 - 23 Barrio Pinares", 
        "Carrera 3 No 16 - 54 Barrio San Fernando", 
        "Calle 50 No 20 - 05 Barrio Álamos", 
        "Carrera 6 No 23 - 33 Barrio Corales"]
        
        return direccion[random.randint(0,19)]

    def mesNumero(self,mes:str)->str:

        diccionarioMes = {'Jan': '01',
                        'Feb': '02',
                        'March':'03',
                        'April': '04',
                        'May': '05',
                        'June': '06',
                        'July': '07',
                        'Aug': '08',
                        'Sept': '09',
                        'Oct': '10',
                        'Nov': '11',
                        'Dec': '12',
                        }
        
        return diccionarioMes[mes]

    def ajustarNumero(self,numeroDia:str)->str:

        if len(numeroDia) == 1:
            numeroDia = '0'+numeroDia
            return numeroDia
        
        return numeroDia
    
    def invertirMesDia(self,lista):
        valorMes = lista[2]
        lista[2] = lista[1]
        lista[1] = valorMes
        return lista

    def formatoFecha(self)->str:
        self.fecha = self.organizarCadena(self.fecha)
        signos = ['.', ',']
        cadenaFecha = "".join(filter(lambda x: True if x not in signos else False, self.fecha))
        fechaLista = cadenaFecha.strip(" ").split(" ")
        # print(fechaLista[0])
        fechaLista[0] = self.mesNumero(fechaLista[0])
        fechaLista[1] = self.ajustarNumero(fechaLista[1])
        fechaLista = fechaLista[::-1]
        fechaLista = self.invertirMesDia(fechaLista)
        fechaFormatoDjango = ""
        for indice in range(len(fechaLista)):
            if indice != len(fechaLista)-1:
                fechaFormatoDjango += fechaLista[indice] + "-"
            else:
                fechaFormatoDjango += fechaLista[indice]
            

        self.fecha = fechaFormatoDjango

    @classmethod
    def cargarJson(cls,ruta)->dict:
        with open(ruta, encoding='utf-8') as scrapi:
            diccionario = json.load(scrapi)
            # print(cargar)
        return diccionario


    @staticmethod
    def generarRegistroBd(denuncia,victima,agresor):
        return Denuncia.objects.create(agresor = agresor, victima = victima, fecha = denuncia.fecha, descripcion = denuncia.descripcion, ubicacion = denuncia.ubicacion, ciudad = denuncia.ciudad)
    # def generarRegistrosScrapy()->None:
    #     listaDiccionarios = cargarJson()
    #     for elementoLista in listaDiccionarios:
    #         fechaDjango = formatoFecha(elementoLista['FechaDenuncia'])
    #         victima = VictimaRepresentacion.objects.create(nombre = organizarCadena(elementoLista['NombreVictima']),primerApellido = organizarCadena(elementoLista['PrimerApellido']),segundoApellido = organizarCadena(elementoLista['SegundoApellido']),tipoDocumento = organizarCadena(elementoLista['TI-Victima']),numeroDocumento = organizarCadena(elementoLista['NumDocumento-Victima']),ciudadNacimiento = organizarCadena(elementoLista['CiudadNa-Victima']),ciudadRecidencia = organizarCadena(elementoLista['CiudadRe-Victima']))

    #         victima = VictimaScrapy(nombre = elementoLista['NombreVictima'],primerApellido = elementoLista['PrimerApellido'],segundoApellido = elementoLista['SegundoApellido'],tipoDocumento = elementoLista['TI-Victima'],numeroDocumento = elementoLista['NumDocumento-Victima'],ciudadNacimiento = elementoLista['CiudadNa-Victima'],ciudadRecidencia = elementoLista['CiudadRe-Victima'])

    #         agresor = Agresor.objects.create(nombre = organizarCadena(elementoLista['Nombre-Agresor']),primerApellido = organizarCadena(elementoLista['Apellido-Agresor']),segundoApellido = organizarCadena(elementoLista['SegundoApellido-Agresor']),tipoDocumento = organizarCadena(elementoLista['Ti-Documento-Agresor']),numeroDocumento = organizarCadena(elementoLista['NumDocumento-Victima']),ciudadNacimiento = organizarCadena(elementoLista['CiudadNa-Agresor']),ciudadResidencia = organizarCadena(elementoLista['CiudadRe-Agresor']))

    #         Denuncia.objects.create(agresor = agresor,victima = victima,fecha = fechaDjango, descripcion = elementoLista['DenunciaDescripcion'], ubicacion = agregarDireccion(), ciudad = 'Pereira')


class BibliotecasCasos:
    def __init__(self) -> None:
        self.listaDenuncias = []


class BibliotecaCasosSelenium(BibliotecasCasos):
    def __init__(self) -> None:
        super().__init__()

    def cargarScrapy(self)->dict:
        self.listaCasos = scrapyLista()
        return self.listaCasos 

    def listarCasos(self):
        
        self.cargarScrapy()
        
        for elemento in self.listaCasos:

            agresor = AgresorSelenium(nombre=elemento['Demandado'],primerApellio=None,segundoApellido=None)
            victima = VictimaSelenium(nombre= elemento['Victima'], primerApellido=None,segundoApellido=None)
            victima.ajustarIdentidad()
            victimaRegistro = victima.generarModeloBaseDatos(victima)
            agresor.ajustarIdentidad()
            agresorRegistro = agresor.registrarAgresor(agresor)
            if victimaRegistro != None and agresorRegistro != None:
                victima.guardarRegistroBd(victimaRegistro)
                agresor.guardarRegistroBd(agresorRegistro)
                denuncia = DenunciaSelenium(titulo=elemento['#Sentencia'],agresor=agresor,victima=victima,fecha=elemento['Fecha'],descripcion=elemento['Resumen'])
                denunciaRegistro = denuncia.generarRegistroDb(denuncia,victimaRegistro,agresorRegistro)
                denuncia.guardarDenunciaDb(denunciaRegistro)
                self.listaDenuncias.append(denuncia)


class BibliotecaCasosScrapy(BibliotecasCasos):

    def obtenerInformacionJson(self):
        ruta = r'D:\Programacion\Universidad\Software2\ProyectoPrincipal\scarpingPaginaWeb\denuncia_spider.json'
        self.listDiccionario = DenunciaScrapy.cargarJson(ruta=ruta)
        return self.listDiccionario

    def listarCasos(self):
        for elementoLista in self.listDiccionario:
            victima = VictimaScrapy(nombre = elementoLista['NombreVictima'],edad= elementoLista['EdadVictima'],primerApellido = elementoLista['PrimerApellido'],segundoApellido = elementoLista['SegundoApellido'],tipoDocumento = elementoLista['TI-Victima'],numeroDocumento = elementoLista['NumDocumento-Victima'],ciudadNacimiento = elementoLista['CiudadNa-Victima'],ciudadRecidencia = elementoLista['CiudadRe-Victima'])

            victima.ajustarDatos()
            victimaRegistro = victima.generarRegistroDb(victima)

            agresor = AgresorScrapy(nombre= elementoLista['Nombre-Agresor'], primerApellio=elementoLista['Apellido-Agresor'],segundoApellido=elementoLista['SegundoApellido-Agresor'], tipoDocumento= elementoLista['Ti-Documento-Agresor'], numeroDocumento= elementoLista['NumDocumento-Victima'], ciudadNacimiento= elementoLista['CiudadNa-Agresor'], ciudadResidencia=elementoLista['CiudadRe-Agresor'],entidad=False)

            agresor.ajustarDatos()
            agresorRegistro = agresor.generarRegistroDb(agresor)

            denunciaScrapy = DenunciaScrapy(titulo=None, agresor=agresor, victima=victima,fecha= elementoLista['FechaDenuncia'],descripcion= elementoLista["DenunciaDescripcion"], prevenciones = 'No tiene', ubicacion= 'No tiene', ciudad= 'Pereira')

            denunciaScrapy.formatoFecha()
            denunciaScrapy.ubicacion = denunciaScrapy.agregarDireccion()

            denunciaScrapy.generarRegistroBd(denunciaScrapy,victimaRegistro,agresorRegistro)
            
       
        
        
                

            

        




# Importar las librerias necesarias
from functools import reduce
from .models import Victima, Agresor, Denuncia
from Scrapy.ScrapingCorteSelenium import scrapyLista
from .models import *


def filtrarPalabrasVictima(informacion)->list:
    listaDePalabras = ['DE','OFICIO','PROCESADO','OTROS', 'Y','OFICIOS','OTRO','OTRA', 'OTRAS', 'SALA','SEGUIMIENTO',""]
    listaFiltrada = list(filter(lambda x: True if x not in listaDePalabras else False, listaDePalabras))
    if len(listaDePalabras) != 0:
        return listaDePalabras
    else:
        return []
    



# Funcion para identificar los apellidos y nombres de las victimas
def guardarVictima(informacion:str)->Victima:
    longitudInformacion = len(informacion)
    listaPalabras = filtrarPalabrasVictima(informacion)
    if len(informacion) > 7:
        return "Hay demasiadas palabras en el valor del nombre"
    elif len(listaPalabras) == 1:
        victima = Victima.constructorSeleniumUniNombre(nombre=listaPalabras[0])
        return victima
    elif len(listaPalabras) == 2:
        victima = Victima.constructorSeleniumNombreApellido(nombre=listaPalabras[0],segundoApellido=listaPalabras[2])
        return victima
    elif len(listaPalabras) == 3:
        victima = Victima.constructorSeleniumIdentidadCompleta(nombre=listaPalabras[0],primerApellido=listaPalabras[1], segundoApellido=listaPalabras[2] )
        return victima
    elif len(listaPalabras) == 4:
        victima = Victima.constructorSeleniumIdentidadCompleta(nombre=listaPalabras[0],primerApellido=listaPalabras[2], segundoApellido=listaPalabras[3])
        return victima
    elif listaPalabras == []:
        return "No es posible determinar el nombre de la persona"
    


# Determina si se puede determinar el tipo de agresor y tambien su identidad.
def determinarValidesAgresor(lista:list)->bool:
    # Lista de palabras que determinan si es posible validar la identidad de la entidad o la persona.
    listaPalabras = ['y', 'otros']

    # Recorrer la lista de palabras que estan completamente en minuscula.
    for palabra in lista:
        # Condicion para verificar si la palabras es una de las palabras que verifican que no es un usuario que se puede guardar en la base de datos.
        if palabra in lista:
            # Retorna verdadero, afirmando que el usuario no es valido para guardar en la base de datos.
            return True
    
    # Retorna falso, afirmando que el usuario es valido para ser guardado en la base de datos.
    return False


# Determina que tipo de agresor es si una entidad o si es una persona
def filtrarPalabrasAgresor(informacion)->tuple:
    listaMinusculas = list(map(lambda x: x.lower(), informacion))
    verificarValides = determinarValidesAgresor(listaMinusculas)
    if verificarValides == True:
        # El cero representa que no es valido
        return verificarValides,0
    
    listaPalabras = ['tribunal', 'superior', 'judicial','ley','municipio','ministerio','periodico','fundacion', 'fiscalia', 'fondo', 'universidad', 'fonvivienda','consejo', 'juzgado', 'institución', 'sas', 'comisaria', 'eps', 'secretaria','fonvivienda','alcaldia','codigo']

    for palabras in listaMinusculas:
        if palabras in listaPalabras:
            # El uno representa que este usuario es valido para ser guardado como entidad
            return True,1
    
    # El uno representa que este usuario es valido para ser guardado como persona
    return False,1



def guardarAgresor(informacion:str)->Agresor:
    tipoAgresor = filtrarPalabrasAgresor(informacion)
    if tipoAgresor[0] == True and tipoAgresor[1] == 1:
        nombreEntidad = reduce(lambda x,y: x+y, informacion)
        agresor = Agresor.seleniumConstructorEntidad(nombreEntidad)
        return agresor
    elif tipoAgresor[0] == False:
        if len(informacion) == 1:
            agresor = Agresor.seleniumConstructorAgresoPersonaUniNombre(informacion[0])
            return agresor
        elif len(informacion) == 2:
            agresor = Agresor.seleniumConstructorAgresorPersonaNombreApellido(informacion[0],informacion[1])
            return agresor
        elif len(informacion) == 3:
            agresor = Agresor.seleniumConstructorAgresorIdentidadCompleta(informacion[0], informacion[1], informacion[2])
            return agresor
        elif len(informacion) == 4:
            agresor = Agresor.seleniumConstructorAgresorIdentidadCompleta(informacion[0],informacion[2],informacion[3]) 
            return (agresor,tipoAgresor)
    else:
        return 'No se puede guardar el agresor.'


# Funcion para llenar las tablas con el scrapy realizado con el software de selenium.
def llenarTablasScrapySelenium()->None:
    # Se trae la lista de diccionarios con la informacion que recopilo selenium.
    listaCasos = scrapyLista()
    
    # Se recorre la lista de diccionarios para desempaquetar la informacion.
    for diccionario in listaCasos:
        # Convertir el nombre con los apellidos del demandantes en una lista.
        listaNombreVictima = diccionario["Demandante"].split(" ")
        listaNombreAgresor = diccionario["Demandado"].split(" ")
        # Crea un registro en la base de datos 
        agresor = guardarAgresor(listaNombreAgresor)
        victima = guardarVictima(listaNombreVictima)

        if isinstance(agresor,Agresor) and isinstance(victima,Victima):
            agresor.save()
            victima.save()
            Denuncia.constructorSelenium(agresor=agresor,victima=victima,fecha=diccionario["Fecha"],descripcion = diccionario["Resumen"])




from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pprint as pp


def obtenerSentencia(texto):
    patron1 = r"https:\/\/www\.corteconstitucional\.gov\.co\/relatoria\/[A-Za-z0-9\/_.-]+\.htm"
    numeroSentencia = re.findall(patron1, str(texto))


    sentenciasFinales = []
    for i in numeroSentencia:
        titulos = i.replace(".htm", "").split("/")[-1]
        sentenciasFinales.append(titulos)
    return sentenciasFinales


def obteneFechas(texto):
    # Encontrar todas las celdas <td> dentro de <tbody> que tienen la clase especificada
    fechas = texto.find_all('td', class_="text-center")

    # Filtrar y almacenar solo las fechas que coinciden con el formato 'YYYY-MM-DD'
    # Expresión regular para el formato de fech
    fecha_formato = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    fechas_validas = []
    for fecha in fechas:
        texto_fecha = fecha.get_text(strip=True)
        # Verifica si coincide con el formato

        if fecha_formato.match(texto_fecha):
            fechas_validas.append(texto_fecha)
        elif texto_fecha == "":
            fechas_validas.append(None)
    tuplas_fechas = []
    contador = 0
    for i in range(0, len(fechas_validas), 2):
        tuplas = fechas_validas[i], fechas_validas[i+1]
        tuplas_fechas.append(tuplas)
        contador += 2

    return tuplas_fechas


def obtenerTemaResumen(contenido):
    # Encontrar todas las celdas <td> dentro de <tbody> que tienen la clase especificada
    TemaResumen = contenido.find_all('td', class_="text-justify hidden-xs")
    tema_resumenLista = []
    for Tema in TemaResumen:
        texto = Tema.get_text(strip=True)
        # print("---------------------")
        # print(texto)
        # Buscar el texto después de "TEMA:" y antes de "RESUMEN:"
        if "TEMA:" in texto and "RESUMEN:" in texto:
            tema = texto.split("TEMA:", 1)[1].split("RESUMEN:", 1)[0].strip()
        else:
            tema = "Tema no encontrado"
        # Buscar el texto después de "RESUMEN:"
        if "RESUMEN:" in texto:
            resumen = texto.split("RESUMEN:", 1)[1].strip()
        else:
            resumen = "Resumen no encontrado"
        # print("----------------------")
        # print("TEMA")
        # print(tema)
        # print("RESUMEN")
        # print(resumen)
        tupla = tema, resumen
        tema_resumenLista.append(tupla)
    return tema_resumenLista

# def recoleccionModal(texto):


def tuplaDemandanteDemandado(texto):
    listaTuplas = []
    tupla = texto.split("Demandante:", 1)[1].split("Demandado:")


def crearListaDiccionarios(sentencias, fechas, temasResumenes):
    listaCasos = []
    print(len(fechas))
    print(len(sentencias))
    print(len(temasResumenes))
    # for sentencia in sentencias:
    for indice in range(len(sentencias)):
        listaCasos.append({"#Sentencia": sentencias[indice], "Fecha": fechas[indice][0], "Tema": temasResumenes[indice]
                          [0], "Resumen": temasResumenes[indice][1], "Demandado": None, "Demandante": None})
    return listaCasos

# Buscar el contenido completo de la ventana modal
# contenido_completo_modal = soup.find('div', id='Modal_prov_Info')


def scrapingtablabloy(soup):
    tbody = soup.find('tbody')

    if tbody:

        sentencias = obtenerSentencia(tbody)
        # pp.pprint(sentencias)
        
        fechas = obteneFechas(tbody)
        # pp.pprint(fechas)
        # # print(fechas)
        # # print(fechas)

        tuplaTemaResumen = obtenerTemaResumen(tbody)
        # print(tuplaTemaResumen)
        # print(sentencias)
        post = crearListaDiccionarios(sentencias, fechas, tuplaTemaResumen)


    else:
        print("No se encontró <tbody> en el documento.")
    return post

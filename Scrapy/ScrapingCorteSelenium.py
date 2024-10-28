# para controlar el navegador
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
# para esperar a que cargue la pagina manejando los tiempos
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# para especificar en que etiqueta esta
from selenium.webdriver.common.by import By
import time
from .ScrapingCorte import *
from bs4 import BeautifulSoup
# import pprint as pp
from pathlib import Path
from django.conf import settings

# Ruta relativa usando pathlib


def scrapyLista() -> list:
    # opciones de navegacion
    edge_options = Options()
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument('--start-maximized')
    edge_options.add_argument('--disable-extensions')
# 
    driver_path = Path(settings.BASE_DIR) / "Scrapy" / "edgedriver_win64" / "msedgedriver.exe"
    # print(driver_path)
    service = Service(executable_path=str(driver_path))
    # driver_path = Service('./edgedriver_win64/msedgedriver.exe')

    driver = webdriver.Edge(service=service, options=edge_options)

    # inicializamos el navegador

    driver.get('https://www.corteconstitucional.gov.co/relatoria/buscador_new/?searchOption=texto&fini=1992-01-01&ffin=2024-10-15&buscar_por=violencia+de+genero&accion=search&verform=si&slop=1&buscador=buscador&qu=search_principalMatch&maxprov=100&OrderbyOption=des__score&tot_provi_found=5144&tot_provi_show=100')

    listaFinal = []

    paginas = 1
    contadorIterador = 0
    while paginas <= 4:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        info = scrapingtablabloy(soup)
        listaFinal += info
        # pp.pprint(listaFinal)
        driver.execute_script("window.scrollTo(0, 0);")
        contador = 1
        while contador <= 25:
            print(contador)
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, f'//*[@id = "tablet_results"]/tbody/tr[{contador}]/td[1]/p/a'))
            ).click()

            # Esperamos a que la ventana modal esté visible
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="div_modal_info"]/div[2]'))
            )
            time.sleep(2)
            Demandante = driver.find_element(
                By.XPATH, '/html/body/div[4]/div/div/div[2]/div/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[2]')
            Demandado = driver.find_element(
                By.XPATH, '/html/body/div[4]/div/div/div[2]/div/div[1]/div/div[2]/div[1]/div[2]/div[3]/div[2]')
            infoDenuncia = Demandante.text, Demandado.text
            # print(infoDenuncia)
            time.sleep(1)
            listaFinal[contadorIterador]["Demandante"] = infoDenuncia[0]
            listaFinal[contadorIterador]["Demandado"] = infoDenuncia[1]
            contadorIterador += 1
            # pp.pprint(listaFinal)

            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'span[aria-hidden=true]'))
            ).click()
            time.sleep(1)
            contador += 1
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'a.page-link.next'))
        ).click()
        print()
        time.sleep(3)
        paginas += 1

    driver.quit()
    return listaFinal

# scrapyLista()
import os
import sys
from .models import Victima, Agresor, Denuncia
from Scrapy.ScrapingCorteSelenium import scrapyLista
# sys.path.append('Scrapy')
# from ScrapingCorteSelenium import scrapyLista
# from Scrapy.
# from Scrapy.ScrapingCorteSelenium import scrapyLista
# from Scrapy.ScrapingCorteSelenium import scrapyLista
# from ..Scrapy.ScrapingCorteSelenium import scrapyLista

# sys.path.append(os.path.abspath(".."))
# sys.path.append('../Scrapy')
# Agregar el directorio superior al sys.path
# ruta_proyecto = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.append(ruta_proyecto)

# Ahora importar la función de forma absoluta


def creaLista():
    listaCasos = scrapyLista()

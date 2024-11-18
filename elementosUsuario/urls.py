from django.urls import path,include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'victima',VistaVictima, 'victima')
router.register(r'agresor',VistaAgresor, 'agresor')
router.register(r'denuncia',VistaDenuncia, 'denuncia')
urlpatterns = [
  path('Api/v1/', include(router.urls)),
  path('docs/',include_docs_urls(title='Casos de violencia'))
]
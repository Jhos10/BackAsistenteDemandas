from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
# Create your views here.

class VistaVictima(viewsets.ModelViewSet):
  serializer_class = VictimaSerializer
  queryset = Victima.objects.all()

class VistaAgresor(viewsets.ModelViewSet):
  serializer_class = AgresorSerializer
  queryset = Agresor.objects.all()

class VistaDenuncia(viewsets.ModelViewSet):
  serializer_class = CasoViolenciaSerializer
  queryset = Denuncia.objects.all()

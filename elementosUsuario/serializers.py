from rest_framework import serializers
from .models import *
class VictimaSerializer(serializers.ModelSerializer):
  class Meta:
    model = Victima
    fields = '__all__'

class AgresorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Agresor
    fields = '__all__'

class CasoViolenciaSerializer(serializers.ModelSerializer):
  class Meta:
    model = Denuncia
    fields = '__all__'

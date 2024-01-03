from rest_framework import serializers
from app3.models import medical

class medicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = medical
        fields = '__all__'
from rest_framework import serializers
from .models import vendors,sneakers_data

class vendorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = vendors
        fields = '__all__'


class sneakersSerializer(serializers.ModelSerializer):
    class Meta:
        model = sneakers_data
        fields = '__all__'




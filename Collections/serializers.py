from rest_framework import serializers
from rest_framework import permissions
from .models import Collection,CollectedCustomer



class CollectionSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('__all__')

class CollectedCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model =CollectedCustomer
        fields = ('__all__')
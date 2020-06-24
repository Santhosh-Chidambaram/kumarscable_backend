from rest_framework import serializers
from rest_framework import permissions
from .models import Collection,CollectedCustomer
from Customers.serializers import CustomerSerializer
class CollectionSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('__all__')

class CollectedCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model =CollectedCustomer
        fields = ('__all__')
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['customer'] = CustomerSerializer(instance.customer).data.get('name')
        
        return response
    
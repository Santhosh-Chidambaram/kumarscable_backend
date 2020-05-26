from rest_framework import serializers
from rest_framework import permissions
from .models import CustomerReport,Customer
from Setupboxes.serializers import SetupBoxSerializer

class CustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = ('__all__')
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['setupbox'] = SetupBoxSerializer(instance.setupbox).data.get('boxno')
        return response
    


class CustomerReportSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomerReport
        fields = ('__all__')

    


from rest_framework import serializers
from rest_framework import permissions
from .models import CustomerReport,Customer
from Setupboxes.serializers import SetupBoxSerializer

class CustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = ('__all__')

    


class CustomerReportSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomerReport
        fields = ('__all__')



from rest_framework import serializers
from rest_framework import permissions
from .models import CustomerReport,Customer,Packages,Channels

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Packages
        fields = ('__all__')

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channels
        fields = ('__all__')


class CustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = ('__all__')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['packages'] = PackageSerializer(instance.packages,many=True).data
        response['channels'] = ChannelSerializer(instance.channels,many=True).data
       
        return response
class CustomerPaymentSerializer(serializers.ModelSerializer):
    class Meta :
        model = Customer
        fields = ('payment_date','phone','payment_status')    


class CustomerReportSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomerReport
        fields = ('__all__')
    


    


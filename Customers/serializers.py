from rest_framework import serializers
from rest_framework import permissions
from .models import CustomerReport,Customer,Packages,Channels
from django.contrib.auth.models import User

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
    

class CustomerRegistration(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    stbno = serializers.CharField(max_length=8)
    class Meta:
        model = User
        fields = ('username','password','password2','stbno')
    
    def save(self):
        user = User(username=self.validated_data['username'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        stbno = self.validated_data['stbno']
        cus = Customer.objects.filter(stbno=stbno)

        if password != password2 :
            raise serializers.ValidationError({'password':'Passwords must match'})
        if not cus.exists():
            raise serializers.ValidationError({'stb':'stb does not exists'})
        user.set_password(password)
        user.save()
        u_id = User.objects.get(username=user.username)
        cus.update(user=u_id.pk,customer_type='internet')


        return user


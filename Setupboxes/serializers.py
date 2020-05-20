from rest_framework import serializers
from rest_framework import permissions
from .models import  SetupBox,Channel

class SetupBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetupBox
        fields = ('__all__')
  

class ChannelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Channel
        fields = ('__all__')

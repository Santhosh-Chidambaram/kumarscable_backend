from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework import status
from .models import *
from rest_framework.decorators import api_view,permission_classes
from rest_framework.mixins import ListModelMixin
from .serializers import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
import json
import datetime
from django.shortcuts import get_object_or_404,get_list_or_404

# Create your views here.


class ChannelList(APIView,ListModelMixin):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        data = Channel.objects.all()
        serializer = ChannelSerializer(data,context={'request':request},many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = ChannelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class PackagesList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        bqts = Bouquet.objects.all()
        bcbqts = BroadcastBouquet.objects.all()
        return Response({
           "bouquets":[{
               "id":b.id,
               "name":b.name,
               "price":b.price


            }for b in bqts],
            "bcbouquets":[{
                "id":b.id,
               "name":b.name,
               "price":b.price

            }for b in bcbqts]
            
        })



#STB API Views
class STBList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        try:
            stbs = SetupBox.objects.all()
        except SetupBox.objectDoesNotExist:
            pass
        
        return Response(
            {
            "id":stb.id,
            "boxno":stb.boxno,
            "base_price":stb.base_price,
            "start_date":stb.start_date,
            "end_date":stb.end_date,
            "additional_price":stb.additional_price,
            "gst_price":stb.gst_price,
            "total_price":stb.total_price,
            "addon_packages":[ {"name":p.name,"id":p.id,"price":p.price}for p in stb.addon_packages.all()],
            "bouquets":[ {"name":p.name,"id":p.id,"price":p.price}for p in stb.bouquets.all()],
            "bcbouquets":[ {"name":p.name,"id":p.id,"price":p.price}for p in stb.broadcast_bouquets.all()]

        }for stb in stbs)

    def post(self,request):
        serializer = SetupBoxSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

 
@api_view(['GET', 'PUT', 'DELETE'])
def STBDetail(request, pk):

    try:
        stb = SetupBox.objects.get(pk=pk)
    except SetupBox.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SetupBoxSerializer(stb)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SetupBoxSerializer(stb, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        stb.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def stbsCount(request):
    return Response({
       "stbs_count":SetupBox.objects.all().count()
    })

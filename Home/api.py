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



class InvoiceView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,boxno):  
        try:
            q_box = Customer.objects.filter(setupbox__boxno=boxno)
        except Customer.objectDoesNotExist:
            return Response({"Customer Does Not Exist"},status=status.HTTP_404_NOT_FOUND)
        
     
        return Response({
                    "id":s.id,
                    "name":s.name,
                    "street":s.street,
                    "phone":s.phone,
                    "setupbox":
                        {
                        
                        "boxno":s.setupbox.boxno,
                        "base_package":s.setupbox.base_package,
                        "bouquets":[{
                            "id":p.id,"name":p.name }for p in s.setupbox.bouquets.all()
                            ]
                        ,
                        "bcbouquets":[{
                            "id":p.id,"name":p.name }for p in s.setupbox.broadcast_bouquets.all()
                            ],
                        "addon_packages":[{
                            "id":p.id,"name":p.name }for p in s.setupbox.addon_packages.all()
                            ],
                        "start_date":s.setupbox.start_date,
                        "end_date":s.setupbox.end_date,
                        "base_price":s.setupbox.base_price,
                        "add_price":s.setupbox.additional_price,
                        "gst":s.setupbox.gst_price,
                        "total_price":s.setupbox.total_price
                        },
                    "payment_amount":s.payment_amount

                    } for s in q_box)
            






@api_view(['GET'])
def getUserId(request):
    userid =User.objects.get(pk=request.user.pk)
    return Response({
        "userid":userid.pk
    })

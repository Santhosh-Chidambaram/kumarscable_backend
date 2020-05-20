from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework import status
from .models import Customer,CustomerReport
from rest_framework.decorators import api_view,permission_classes
from rest_framework.mixins import ListModelMixin
from .serializers import CustomerReportSerializer,CustomerSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.models import User
import json
import datetime
from django.shortcuts import get_object_or_404,get_list_or_404


#Customer API Views

@permission_classes([IsAuthenticated,])
@api_view(['GET', 'PUT'])
def CustomerPaymentUpdate(request, pk):

    try:
        cs = Customer.objects.get(pk=pk)
        
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CustomerSerializer(cs)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CustomerSerializer(cs, data=request.data)
        crserializer = CustomerReportSerializer(data=request.data)
        if serializer.is_valid() and crserializer.is_valid() :
            serializer.save()
            crserializer.save()
            return Response(serializer.data)
        return Response(crserializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        pass


class GetCustomer(APIView):
    permission_classes = (IsAuthenticated,)
    def  get(self,request,boxno):
        try:
            q_box = Customer.objects.filter(setupbox__boxno=boxno)
        except Customer.objectDoesNotExist:
            return Response({"Customer not found"},status=status.HTTP_404_NOT_FOUND)
        
        return Response({
                    "id":s.id,
                    "name":s.name,
                    "street":s.street,
                    "phone":s.phone,
                    "payment_status":s.payment_status,
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


@permission_classes([IsAuthenticated,])
@api_view(['GET', 'PUT', 'DELETE'])
def CustomerDetail(request, pk):

    try:
        cs = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CustomerSerializer(cs)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CustomerSerializer(cs, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        cs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CustomerList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        cus = Customer.objects.all()
        tab = request.GET.get('tab')

        if tab :
            cd = cus.filter(payment_status=tab)

            return Response({
                "count":cd.count(),
                "id":c.id,
                "name":c.name,
                "street":c.street,
                "phone":c.phone,
                "setupbox":c.setupbox.boxno,
                "payment_amount":c.payment_amount,
                "payment_status":c.payment_status,


                }for c in cd
            )

        else:
    
            return Response({
                "id":c.id,
                "name":c.name,
                "street":c.street,
                'phone':c.phone,
                "setupbox":c.setupbox.boxno,
                "payment_amount":c.payment_amount,
                "payment_status":c.payment_status,
            }for c in cus)


    def post(self,request):
        serializer = CustomerSerializer(data=request.data)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def customersCount(request):
    return Response({
       "customers_count":Customer.objects.all().count()
    })

@api_view(['POST'])
def setAllCustomersToUnpaid(request):
    Customer.objects.all().update(payment_status='unpaid')
    return Response({"All Customers Payment Status Changed to Unpaid"},status=status.HTTP_200_OK)

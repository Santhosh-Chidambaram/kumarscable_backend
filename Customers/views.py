from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework import status
from .models import (Customer,CustomerReport,
Packages,Channels,PackageRequest,
OnlineTransaction,UserComplaint)

from rest_framework.decorators import api_view,permission_classes
from rest_framework.mixins import ListModelMixin

from .serializers import (CustomerReportSerializer,
CustomerSerializer,PackageSerializer,ChannelSerializer,
CustomerPaymentSerializer,CustomerRegistration,PackageRequestSerializer,UserComplaintSerializer,OnlineTransactionSerializer)
from Collections.serializers import CollectedCustomerSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.models import User
import json
import datetime
from django.shortcuts import get_object_or_404,get_list_or_404
from django.http import Http404
from django.db import IntegrityError
from  Collections.models import Collection
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
client = razorpay.Client(auth=("#key","#secret"))


#Customer Authentication Views
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username':user.username,
            
            
        })

@csrf_exempt
@api_view(['POST'])
def CustomerRegisterView(request):
        serializer = CustomerRegistration(data=request.data)

        if serializer.is_valid():
            serializer.save()
            user_obj = User.objects.get(username=serializer.data['username'])
            token = Token.objects.get(user=user_obj)
            return Response(
                {
                    'token':str(token),
                    'username':user_obj.username,
                    'user_id':user_obj.pk,
                    'email':user_obj.username
                
                }
                ,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



#Customers App Views
@api_view(['GET'])
def CustomerDataView(request,pk):
    cus_obj = Customer.objects.filter(user=pk)
    return Response(
        
            {
                "id":c.id,
                "name":c.name,
                "street":c.street,
                "phone":c.phone,
                "customer_type":c.customer_type,
                "due_amount":c.due_amount,
                "due_months":c.due_months,
                "payment_status":c.payment_status,
                "stbno":c.stbno,
                "payment_amount":c.payment_amount,
                "box_status":c.box_status,
                "packages":[
                {   
                    "id":p.id,
                    "name":p.name
                }
                for p in c.packages.all()
                ],
                "channels":[
                    {   
                        "id":ch.id,
                        "name":ch.name
                    }for ch in c.channels.all()
                ]
               


            }
            for c in cus_obj
    )


@csrf_exempt
@api_view(['POST'])
def PackageRequestView(request):
        serializer = PackageRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def GetPackageRequestView(request,id):
        pack_reqs = PackageRequest.objects.filter(customer=id)
        return Response({
            "id":p.id,
            "customer":p.customer.username,
            "date":p.date,
            "request_status":p.request_status,
            "payment_status":p.payment_status,
            "payment_mode":p.payment_mode,
            "packs":{
                "packages":[pck.name for pck in p.packages.all()],
                "channels":[pck.name for pck in p.channels.all()]
            }
        }for p in pack_reqs)
        #return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def addSTBView(request,boxno):
    customer = Customer.objects.get(stbno=boxno)
    customer.user =request.user
    customer.save()
    return Response({"User Update successfully"})



class RegisterCompaint(APIView):

    def get(self,request):
        complaints = UserComplaint.objects.filter(customer=request.user.id)
        return Response({
            "id":p.id,
            "customer":p.customer.username,
            "date":p.date,
            "status":p.status,
            "resolved_date":p.resolved_date,
            "complaint":p.complaint,
            "complaint_type":p.complaint_type,
     
        }for p in complaints)



    def post(self,request):
        serializer = UserComplaintSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    








#Customer API Views
class getUserId(APIView):
    showPhone = False
    
    def get(self,request):
        userid =User.objects.get(pk=request.user.pk)
        return Response({
            "userid":userid.pk,
            "showPhoneField":self.showPhone,
        })
    def post(self,request):
        userid =User.objects.get(pk=request.user.pk)
        shw = request.POST.get('showPhoneField')
        self.showPhone = shw
        return Response({
            "userid":userid.pk,
            "showPhoneField":self.showPhone,
        })


@permission_classes([IsAuthenticated,])
@api_view(['GET', 'PUT'])
def CustomerPaymentUpdate(request, pk):

    try:
        cs = Customer.objects.get(pk=pk)
        
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        userid = request.GET.get('userid')
        if userid:
            
            return Response({'Hi'})
        else:
            cr = CustomerReport.objects.filter(customer=pk)
            return Response({
            "reports":[
                {
                    "id":c.id,
                    "customer_name":c.customer_name,
                    "payment_date":c.payment_date,
                    "payment_amount":c.customer.payment_amount,
                }
                for c in cr
            ]
            
            }
            
            )


    elif request.method == 'PUT':
        cus_id = request.data.get('customer')
        stb = request.data.get('stb')
        try:
            cus = get_object_or_404(Customer,id=cus_id)
            serializer = CustomerPaymentSerializer(cs, data=request.data)
            crserializer = CustomerReportSerializer(data=request.data)
            collection_serializer = CollectedCustomerSerializer(data=request.data)
            otserializer = OnlineTransactionSerializer(data=request.data)
            online_mode = request.data.get('payment_mode')

            if cus.stbno == stb:
                try:
                    if not online_mode == 'online' :
                        if serializer.is_valid()  and crserializer.is_valid() and collection_serializer.is_valid():
                            serializer.save()
                            crserializer.save()
                            collection_serializer.save()
                            return Response(collection_serializer.data)
                        elif serializer.errors:
                            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                        elif crserializer.errors:
                            return Response(crserializer.errors,status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response(collection_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                    else :
                        if serializer.is_valid()  and crserializer.is_valid() and collection_serializer.is_valid() and otserializer.is_valid():
                            serializer.save()
                            crserializer.save()
                            collection_serializer.save()
                            otserializer.save()
                            return Response(serializer.data)
                        elif serializer.errors:
                            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                        elif crserializer.errors:
                            return Response(crserializer.errors,status=status.HTTP_400_BAD_REQUEST)
                        elif otserializer.errors:
                            return Response(otserializer.errors,status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response(collection_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                except IntegrityError as e:

                    return Response({"Customer has already paid"}, status=status.HTTP_403_FORBIDDEN)
                
            return Response({"Invalid Customer Id or Boxnumber"}, status=status.HTTP_404_NOT_FOUND)
        except Http404:
           return Response({"Invalid Customer Id or Boxnumber"}, status=status.HTTP_404_NOT_FOUND)
        
        

    else:
        pass
        


class GetCustomer(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def  get(self,request,boxno):
        q_box = Customer.objects.filter(stbno=boxno)
        if q_box:
            serializer = CustomerSerializer(q_box,many=True)
            order_amount = serializer.data[0]['payment_amount']*100
            order_currency = 'INR'
            order_receipt = 'kc_rcpt_11'
            result = client.order.create(dict(amount=order_amount,currency=order_currency,receipt=order_receipt,payment_capture='0'))
            order_id = result['id']
            order_status = result['status']
            if order_status =='created':
                return Response({
                    "order_id":order_id,
                    "cusData":serializer.data[0]
                    
                })
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"Customer not found"},status=status.HTTP_404_NOT_FOUND)

            


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
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
           return Response("STB Already exits",status=status.HTTP_403_FORBIDDEN) 
           
      

    elif request.method == 'DELETE':
        cs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CustomerList(APIView):
    #permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self,request):
       customer = Customer.objects.all()
       serializer = CustomerSerializer(customer,many=True)
       return Response(serializer.data)

    def post(self,request):
        serializer = CustomerSerializer(data=request.data)
        
        try:

            if serializer.is_valid():
                serializer.save()
                data1 = {
                    "customer":serializer.data.get('id'),
                    "payment_date":serializer.data.get('payment_date'),
                }
                crserializer = CustomerReportSerializer(data=data1)
                if crserializer.is_valid():
                    crserializer.save()
                    return Response(serializer.data,status=status.HTTP_201_CREATED)
                return Response(crserializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
           return Response("STB Already exits",status=status.HTTP_403_FORBIDDEN) 
        
            
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def setAllCustomersToUnpaid(request):
    Customer.objects.all().update(payment_status='unpaid')
    return Response({"All Customers Payment Status Changed to Unpaid"},f)



@api_view(['GET'])
def ShareAmountView(request):

    customer = Customer.objects.all()
    total_share = collected_amount = due_amount = 0
    paidcus = customer.filter(payment_status='paid')
    unpaidcus = customer.filter(payment_status='unpaid')
    paid = customer.filter(payment_status='paid').count()
    unpaid = customer.filter(payment_status='unpaid').count()
    active = customer.filter(box_status='active').count()
    deactive = customer.filter(box_status='deactive').count()
    for c in customer:
        total_share+=c.payment_amount
    for c in paidcus:
        collected_amount+=c.payment_amount
    for c in unpaidcus:
        due_amount+=c.payment_amount
    
    #Collections
    date = datetime.datetime.today().strftime("%Y-%m-%d")
    try:
        coll = Collection.objects.filter(date__startswith=date)
    except TypeError:
        return Response({"Object not found"},status=status.HTTP_404_NOT_FOUND)
    total_collection = 0
    total_customer = []
    for c in coll:
        tc={}
        total_collection+=c.collection_amount
        for cc in c.collection_list.all():
            tc={"customer_name":cc.name,"paid_amount":cc.payment_amount,"payment_status":cc.payment_status}
            total_customer.append(tc)

    
    return Response({

        "paidcount":paid,
        "unpaidcount":unpaid,
        "active":active,
        "deactive":deactive,
        "total_share":total_share,
        "due_amount":due_amount,
        "collected_amount":collected_amount,
        "amount":total_collection,
        "customers":len(total_customer),
        "total":customer.count()

    })
   

class ListCustomers(ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = LimitOffsetPagination

@api_view(['GET'])
def PackagesListView(request):
    pack = Packages.objects.all()
    serialzier = PackageSerializer(pack,many=True)
    return Response(serialzier.data)

@api_view(['GET'])
def ChannelsListView(request):
    channel = Channels.objects.all()
    serialzier = ChannelSerializer(channel,many=True)
    return Response(serialzier.data)


@api_view(['PUT'])
def CheckoutView(request,pk):
    if request.method == 'PUT':
        cus_id = request.data.get('customer')
        stb = request.data.get('stb')
        try:
            cus = get_object_or_404(Customer,id=cus_id)
            serializer = CustomerPaymentSerializer(cus, data=request.data)
            crserializer = CustomerReportSerializer(data=request.data)
            collection_serializer = CollectedCustomerSerializer(data=request.data)
            if cus.stbno == stb:
                try:
                    if serializer.is_valid()  and crserializer.is_valid() and collection_serializer.is_valid():
                        serializer.save()
                        crserializer.save()
                        collection_serializer.save()
                        return Response({
                            'name':cus.name,
                            'stbno':cus.stbno,
                            'payment_amount':cus.payment_amount,
                            'payment_status':cus.payment_status,
                            'street':cus.street,
                            'phone':cus.phone
                        })
                    elif serializer.errors:
                        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                    elif crserializer.errors:
                        return Response(crserializer.errors,status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response(collection_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

                except IntegrityError as e:

                    return Response({"Customer has already paid"}, status=status.HTTP_403_FORBIDDEN)
                
            return Response({"Invalid Customer Id or Boxnumber"}, status=status.HTTP_404_NOT_FOUND)
        except Http404:
           return Response({"Invalid Customer Id or Boxnumber"}, status=status.HTTP_404_NOT_FOUND)






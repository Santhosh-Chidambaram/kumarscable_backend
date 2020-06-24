from django.db import models
from django.db.models.signals import post_save,m2m_changed,pre_save,post_init,post_migrate,pre_migrate,pre_init
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from  month.models import MonthField
from django.contrib.auth.models import User

# Create your models here.



#Subscription Packages Model
class Channels(models.Model):
    class Meta:
        verbose_name_plural = "Channels"
    name = models.CharField(max_length=25)
    price =models.FloatField()


    def __str__(self):
        return f"{self.name+''+'('+ str(self.price)+ ')'}"

class  Packages(models.Model):
    class Meta:
        verbose_name_plural = "Packages"
   
    name = models.CharField(max_length=25)
    price =models.FloatField()
    channels_count = models.CharField(max_length=2,blank=True,null=True)
    def __str__(self):
        return f"{self.name+str(self.price)}"


class Customer(models.Model):
    BASE_CHOICES = [
        ('180', 'BASEPACK180'),
        ('230', 'BASEPACK230')
    ]
    CUSTOMER_TYPE = [
        ('normal', 'NORMAL'),
        ('internet', 'INTERNET')
    ]
    lco_admin = models.ForeignKey(User,on_delete=models.CASCADE,null=True,default=1)

    name = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    phone = models.CharField(max_length=10,null=True,blank=True)
    customer_type = models.CharField(choices=CUSTOMER_TYPE,max_length=10,default='normal')
    due_amount = models.FloatField(default=0,null=True)
    due_months = models.CharField(max_length=2,null=True,blank=True)

    
    payment_status = models.CharField(choices=[('paid','PAID'),('unpaid','UNPAID')],max_length=6,default='unpaid')
    payment_date = models.DateTimeField(auto_now_add=False,null=True,blank=True)
    

    stbno = models.CharField(max_length=10)
    base_package = models.CharField(max_length=3, choices=BASE_CHOICES, default='180')
    packages = models.ManyToManyField(Packages,blank=True,related_query_name='packages_set')
    channels = models.ManyToManyField(Channels,blank=True,related_query_name='channels_set')
    card_number=models.CharField(max_length=20,null=True,blank=True)
    start_date = models.DateField(auto_now_add=False,null=True,blank=True)
    end_date = models.DateField(auto_now_add=False,null=True,blank=True)

    base_price = models.FloatField(default=180)
    additional_price = models.FloatField(default=0)
    gst_price = models.FloatField(default=0)
    payment_amount = models.FloatField(default=0)

    box_status = models.CharField(choices=[('active','Active'),('deactive','Deactive')],max_length=10,default='active')
    deactive_reason = models.CharField(null=True,blank=True,max_length=40)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['stbno'], name='stb')
        ]
    def __str__(self):
        return f"{self.name}"
    def save(self, *args, **kwargs):
       self.payment_amount = self.base_price+self.gst_price+self.additional_price 
       super(Customer, self).save(*args, **kwargs) 
 

class CustomerReport(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=50,blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_month = MonthField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['customer', 'payment_month'], name='um')
        ]

    def __str__(self):
        return f"{self.customer_name}"

    def save(self,*args,**kwargs):
        self.customer_name = self.customer.name
        super(CustomerReport,self).save(*args, **kwargs)

# @receiver(post_init,sender = Customer)
# def pre_total_cal(sender,instance,*args,**kwargs):
#     instance.additional_price = 0
#     for c in instance.channels.all():
#             instance.additional_price+=c.price
#     for p in instance.packages.all():
#             instance.additional_price+=p.price
#     instance.payment_amount = instance.base_price+instance.gst_price+instance.additional_price
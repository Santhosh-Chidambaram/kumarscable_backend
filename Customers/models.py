from django.db import models
from django.db.models.signals import post_save,m2m_changed,pre_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from  month.models import MonthField
from django.contrib.auth.models import User
from Setupboxes import models as stbmodels
# Create your models here.

class Customer(models.Model):
    lco_admin = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=50,blank=True)
    street = models.CharField(max_length=50,blank=True)
    phone = models.IntegerField(null=True,blank=True)
    setupbox = models.OneToOneField(to=stbmodels.SetupBox, on_delete=models.CASCADE,null=True,blank=True)
    payment_amount = models.FloatField(default=0)
    payment_status = models.CharField(choices=[('paid','PAID'),('unpaid','UNPAID')],max_length=6,default='unpaid')
    payment_date = models.DateField(null=True,auto_now=False,blank=True)
    def __str__(self):
        return f"{self.name}"

 

class CustomerReport(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=50,blank=True)
    payment_date = models.DateField(db_index=True)
    payment_month = MonthField(auto_now_add=True)
    class Meta(object):
        unique_together = [['customer','payment_month','payment_date']]
   

    def __str__(self):
        return f"{self.customer}"
    def save(self,*args,**kwargs):
        self.customer_name = self.customer.name
        super(CustomerReport,self).save(*args, **kwargs)

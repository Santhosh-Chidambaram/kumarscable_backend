from django.db import models
from django.db.models.signals import post_save,m2m_changed,pre_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from  month.models import MonthField
from django.contrib.auth.models import User
from Customers import models as customermodels
# Create your models here.

#Subscription Packages Model
class Channel(models.Model):
   
    name = models.CharField(max_length=25)
    price =models.FloatField()


    def __str__(self):
        return f"{self.name+''+'('+ str(self.price)+ ')'}"
class  Bouquet(models.Model):
   
    name = models.CharField(max_length=25)
    price =models.FloatField()
    def __str__(self):
        return f"{self.name+str(self.price)}"
class BroadcastBouquet(models.Model):
    
    name = models.CharField(max_length=25)
    price =models.FloatField()
    def __str__(self):
        return f"{self.name+str(self.price)}"

#SetupBox Model
class SetupBox(models.Model):

    class Meta:
        verbose_name_plural = "SetupBoxes"

    BASE_CHOICES = [
        ('180', 'BASEPACK180'),
        ('230', 'BASEPACK230')
    ]
    boxno = models.CharField(max_length=10)
    base_package = models.CharField(max_length=3, choices=BASE_CHOICES, default='180')
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(auto_now_add=False)
    base_price = models.FloatField(default=180)
    additional_price = models.FloatField(default=0)
    gst_price = models.FloatField(default=0)
    total_price = models.FloatField(default=0)
    bouquets = models.ManyToManyField(Bouquet,related_name='bouquets_set',blank=True,related_query_name='bqpack_set')
    broadcast_bouquets = models.ManyToManyField(BroadcastBouquet,related_name='bcbouquets_set',blank=True,related_query_name='bcbqpack_set')
    addon_packages = models.ManyToManyField(Channel,related_name='channels_set',blank=True,related_query_name='clist_set')
    box_status = models.CharField(choices=[('active','Active'),('deactive','Deactive')],max_length=10,default='active')
    deactive_reason = models.CharField(null=True,blank=True,max_length=40)
    def __str__(self):
        return f"{self.boxno}"

    def get_price(self):
        return self.base_price
        
    def save(self, *args, **kwargs): 
        self.total_price = self.base_price+self.gst_price+self.additional_price
        cus = customermodels.Customer.objects.filter(setupbox__boxno=self.boxno)
        if cus:
            cus.update(payment_amount=self.total_price)
            
        super(SetupBox, self).save(*args, **kwargs) 

from django.db import models
from django.db.models.signals import post_save,m2m_changed,pre_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from  month.models import MonthField
from django.contrib.auth.models import User
from Customers import models as customermodels
# Create your models here.

class Collection(models.Model):
    collection_agent = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    collection_list = models.ManyToManyField(to=customermodels.Customer,related_name='collection_customer_set')
    collection_amount = models.FloatField(default=0)

    def __str__(self):
        return f"{self.date}"
    def save(self,*args, **kwargs):
        super(Collection,self).save(*args, **kwargs)


class CollectedCustomer(models.Model):
    collection_agent = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(to=customermodels.Customer,on_delete=models.CASCADE)
    collected_date = models.DateTimeField(auto_now_add=True)
    month = MonthField(auto_now_add=True)
    collected_amount = models.FloatField()
    street = models.CharField(max_length=50,blank=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['customer', 'month'], name='ucc')
        ]

    def __str__(self):
        return f"{self.customer}"
    
    def save(self,*args, **kwargs):
        self.street = self.customer.street    
        super(CollectedCustomer,self).save(*args, **kwargs)

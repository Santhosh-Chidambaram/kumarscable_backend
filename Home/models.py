from django.db import models
from django.db.models.signals import post_save,m2m_changed,pre_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from  month.models import MonthField
from django.contrib.auth.models import User
# Create your models here.

#Carousel
class CarouselSet(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='carousel/')
    def __str__(self):
        return f"{self.name}"

#Contact Form
class ContactForm(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    message = models.TextField(max_length=100)

    def __str__(self):
        return f"{self.name}"





class Notification(models.Model):
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='to_user_set',null=True)
    from_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    collection_start = models.BooleanField(default=False)
    collection_end = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)




# class Payment(models.Model):
#     name = models.CharField(max_length=50)
#     phone = models.IntegerField()
#     amount = models.IntegerField()
    
#     def __str__(self):
#         return f"{self.name}"



#Signals

#Amount Update Signal
# @receiver(post_save,sender=Customer)
# def update_amount(sender,instance,created,*args,**kwargs):
#     if created:
#         instance.payment_amount = instance.setupbox.price+instance.setupbox.additional_price
#         instance.save()
    



#Amount Signals
# @receiver(pre_save,sender=SetupBox)
# def add_price_update(sender,instance,*args,**kwargs):
#     if instance.addon_packages in Package.objects.all() or instance.bouquets in Bouquet.objects.all() or instance.broadcast_bouquets in BroadcastBouquet.objects.all() :
#         add_price = instance.additional_price+instance.package_price()+instance.bouquets_price()+instance.bcbouquets_price()
#         instance.additional_price = add_price
#         pay_amt = instance.price+instance.additional_price
#         Customer.objects.filter(setupbox=instance).update(payment_amount=pay_amt)
  
#     else:
#         add_price = 0
#         add_price = instance.additional_price+instance.package_price()+instance.bouquets_price()+instance.bcbouquets_price()
#         instance.additional_price = add_price
#         pay_amt = instance.price+instance.additional_price
#         Customer.objects.filter(setupbox=instance).update(payment_amount=pay_amt)
        
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

from django.db import models
from django.db.models.signals import post_save,m2m_changed,pre_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from  month.models import MonthField
from django.contrib.auth.models import User
# Create your models here.
class Notification(models.Model):
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='to_user_set',null=True)
    from_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    collection_start = models.BooleanField(default=False)
    collection_end = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)


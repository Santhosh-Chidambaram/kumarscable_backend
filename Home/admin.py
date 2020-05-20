from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import User, Group


admin.site.unregister(User)
admin.site.unregister(Group)



admin.site.register(CarouselSet)
admin.site.register(ContactForm)
admin.site.register(Notification)



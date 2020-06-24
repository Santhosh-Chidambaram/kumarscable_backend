
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "KUMARSCABLE ADMIN"
admin.site.site_title = "KUMARSCABLE ADMIN PORTAL"
admin.site.index_title = "WELCOME TO KUMARSCABLE ADMIN PORTAL"

urlpatterns = [
    path('admin/', admin.site.urls,name="adminpage"),

    path('',include('Collections.urls')),
    path('',include('Dashboard.urls')),
    path('',include('Customers.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
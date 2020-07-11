from django.contrib import admin
from .models import Customer,CustomerReport,Packages,Channels,OnlineTransaction,PackageRequest,UserComplaint
from import_export.admin import ImportExportModelAdmin
from django.urls import path
from django.http import HttpResponseRedirect


@admin.register(Customer)
class CustomerAdminAll(ImportExportModelAdmin):
    change_list_template = "entities/status_changelist.html"
    list_display = ('id','name','street','payment_amount','payment_status','payment_made')
    list_filter = ['payment_status','street',]
    search_fields=('name','id','street','payment_amount')
    ordering = ['id']
    date_hierarchy = 'payment_date'
    list_per_page = 250
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('setallunpaid/', self.set_allunpaid),
  
        ]
        return my_urls + urls

    def set_allunpaid(self,request):
        self.model.objects.all().update(payment_status='unpaid')
        self.message_user(request,"All Customers Changed to Unpaid")
        return HttpResponseRedirect("../")

    def payment_made(self,obj):
        return obj.payment_status == 'paid'
    payment_made.boolean = True

@admin.register(CustomerReport)
class CsReportAdminAll(ImportExportModelAdmin):
    list_display = ('id','customer_name', 'payment_mode', 'payment_amount', 'payment_month','payment_date')
    ordering = ['id']
    list_filter = ('payment_month','payment_date','payment_mode')
    search_fields= ['customer_name']
    date_hierarchy = 'payment_date'
    list_per_page = 250
    readonly_fields = ['payment_month']


@admin.register(Packages)
class PackagesAdmin(ImportExportModelAdmin):
    list_display = ('name','price','channels_count',)
    ordering = ['id']
    list_filter = ['price']
    search_fields= ['name']

@admin.register(Channels)
class ChannelsAdmin(ImportExportModelAdmin):
    list_display = ('name','price',)
    ordering = ['id']
    list_filter = ['price']
    search_fields= ['name']

admin.site.register(OnlineTransaction)
admin.site.register(PackageRequest)
admin.site.register(UserComplaint)
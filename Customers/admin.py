from django.contrib import admin
from .models import Customer,CustomerReport
from import_export.admin import ImportExportModelAdmin
from django.urls import path
from django.http import HttpResponseRedirect
from Setupboxes.models import SetupBox


@admin.register(Customer)
class CustomerAdminAll(ImportExportModelAdmin):
    change_list_template = "entities/status_changelist.html"
    list_display = ('id','name','setupbox','street','payment_amount','payment_status','payment_made')
    list_filter = ['payment_status','street']
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
    list_display = ('id','customer_name', 'payment_month','payment_date')
    ordering = ['id']
    list_filter = ('payment_month','payment_date')
    search_fields= ['customer_name']
    date_hierarchy = 'payment_date'
    list_per_page = 250
    readonly_fields = ['payment_month']
  



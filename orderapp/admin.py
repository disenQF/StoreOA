from django.contrib import admin
from orderapp.models import OrderModel


# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('num', 'title', 'price', 'pay_status', 'pay_type', 'receiver', 'receiver_phone', 'receive_address')
    fields = ('num', 'title', 'price', 'pay_status', 'pay_type', 'receiver', 'receiver_phone', 'receive_address')


admin.site.register(OrderModel, OrderAdmin)

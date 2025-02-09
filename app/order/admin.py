from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated','code']
    list_filter = ['paid', 'created', 'updated','code']
    inlines = [OrderItemInline]

    readonly_fields = ['total_price']
    
    def total_price(self, obj):
        return obj.get_total_cost()
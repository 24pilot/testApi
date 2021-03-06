from django.contrib import admin
from .models import User, Item, Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'item', 'created_at')
    actions = None

    def save_model(self, request, obj, form, change):
        if not obj.customer:
            obj.customer = request.user
        obj.save()


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')


admin.site.register(User)
admin.site.register(Item, ItemAdmin)
admin.site.register(Transaction, TransactionAdmin)

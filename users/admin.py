from django.contrib import admin
from .models import User, Item, Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'item')
    actions = None

    def save_model(self, request, obj, form, change):
        if not obj.customer:
            obj.customer = request.user
        obj.save()


admin.site.register(User)
admin.site.register(Item)
admin.site.register(Transaction, TransactionAdmin)

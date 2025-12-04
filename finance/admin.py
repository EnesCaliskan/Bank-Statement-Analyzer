from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'amount', 'transaction_type', 'user')
    list_filter = ('transaction_type', 'date')
    search_fields = ('description',)
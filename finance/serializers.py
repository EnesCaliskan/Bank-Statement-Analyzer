
from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'date', 'amount', 'currency', 'description', 'category', 'transaction_type', 'unique_hash']
        read_only_fields = ['unique_hash', 'category']
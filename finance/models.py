import hashlib
from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    
    date = models.DateField()
    
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    
    currency = models.CharField(max_length=3, default='TRY')
    description = models.CharField(max_length=255)
    
    category = models.CharField(max_length=50, blank=True, null=True)
    
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    
    unique_hash = models.CharField(max_length=64, unique=True, editable=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.unique_hash:
            unique_string = f"{self.date}{self.amount}{self.description}{self.transaction_type}{self.user.id}"
            self.unique_hash = hashlib.sha256(unique_string.encode('utf-8')).hexdigest()
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} - {self.description} ({self.amount})"
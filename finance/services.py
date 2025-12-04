import csv
import io
from decimal import Decimal
from django.db import transaction
from .models import Transaction

def categorize_transaction(description):
    """Simple keyword analysis to auto-tag transactions."""
    desc = description.lower()
    if any(x in desc for x in ['kira', 'rent']): return 'Rent'
    if any(x in desc for x in ['fatura', 'bill', 'elektrik', 'su', 'internet']): return 'Bills'
    if any(x in desc for x in ['market', 'gıda', 'food']): return 'Groceries'
    if any(x in desc for x in ['maaş', 'salary']): return 'Payroll'
    if any(x in desc for x in ['satış', 'sales']): return 'Income'
    if 'saas' in desc: return 'Software'
    return 'General'

def process_csv_file(file_obj, user):
    """
    Reads a CSV file object and saves transactions atomically.
    Handles BOM (utf-8-sig) and auto-detects delimiter (, or ;).
    """
    
    decoded_file = file_obj.read().decode('utf-8-sig')
    
    io_string = io.StringIO(decoded_file)
    
    sample = io_string.read(1024)
    io_string.seek(0)
    
    try:
        dialect = csv.Sniffer().sniff(sample)
    except csv.Error:
        dialect = 'excel' 

    reader = csv.DictReader(io_string, dialect=dialect)
    
    reader.fieldnames = [name.strip().lower() for name in reader.fieldnames]

    transactions_to_save = []
    
    for row in reader:
        if 'date' not in row:
             found_keys = list(row.keys())
             raise ValueError(f"Column 'date' not found. Found columns: {found_keys}")

        clean_amount = row['amount'].strip()
        
        category = categorize_transaction(row['description'])
        
        t = Transaction(
            user=user,
            date=row['date'],
            amount=Decimal(clean_amount),
            currency=row['currency'],
            description=row['description'],
            transaction_type=row['type'],
            category=category
        )
        transactions_to_save.append(t)

    try:
        with transaction.atomic():
            for t in transactions_to_save:
                t.save()
        return len(transactions_to_save)
        
    except Exception as e:
        raise e
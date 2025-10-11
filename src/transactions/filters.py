import django_filters
from django import forms
from transactions.models import Transaction, Category

class TransactionFilter(django_filters.FilterSet):
    # removed invalid 'empty' kwarg — use label or let django-filter handle empty choice
    transaction_type = django_filters.ChoiceFilter(
        choices = Transaction.TRANSACTION_TYPES,
        field_name = 'type',
        lookup_expr = 'exact',
        label = 'Transaction type',
        empty_label = "All types" 
    )
    
    category = django_filters.MultipleChoiceFilter(
        choices=getattr(Category, 'DEFAULT_CATEGORIES', []),
        field_name='category',
        lookup_expr='in',
        label='Categories',
        widget=forms.SelectMultiple(attrs={'class': 'form-select form-select-sm'})
    )
    
    date = ''
    
    class Meta:
        model = Transaction
        fields = ('transaction_type', 'category')
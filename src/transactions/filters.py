import django_filters
from transactions.models import Transaction

class TransactionFilter(django_filters.FilterSet):
    # removed invalid 'empty' kwarg — use label or let django-filter handle empty choice
    transaction_type = django_filters.ChoiceFilter(
        choices = Transaction.TRANSACTION_TYPES,
        field_name = 'type',
        lookup_expr = 'exact',
        label = 'Transaction type',
        empty_label = "All types" 
    )
    
    class Meta:
        model = Transaction
        fields = ('transaction_type',)
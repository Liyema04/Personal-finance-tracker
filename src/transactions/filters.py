import django_filters
from transactions.models import Transaction

class TransactionFilter(django_filters.FilterSet):
    transaction_type = django_filters.ChoiceFilter(
        choices = Transaction.TRANSACTION_TYPES,
        field_name = 'type',
        lookup_expr = 'iexact',
        empty = 'Any', 
    )
    
    class Meta:
        model = Transaction
        fields = ('transaction_type',)
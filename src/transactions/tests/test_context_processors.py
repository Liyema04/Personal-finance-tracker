from django.test import RequestFactory
from transactions.context_processors import sidebar_context

def test_sidebar_context_transactions():
    factory = RequestFactory()
    request = factory.get('/transactions/')
    request.resolver_match = type('ResolverMatch', (), {'url_name': 'list_transaction'})
    
    context = sidebar_context(request)
    assert context['active_links']['transactions'] is True
    assert context['current_module'] == 'transactions'
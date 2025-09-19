def sidebar_context(request):
    current_url_name = request.resolver_match.url_name
    current_url_path = request.path
    
    # Get Query parameters
    transaction_type = request.GET.get('transaction_type')
    
    
    # Define which URLs belong to which sections
    context = {
        'active_links': {
            # Main - (Sidebar)
            'dashboard': current_url_name == 'dashboard',
            'transactions': current_url_name in ['list_transaction', 'edit_tranaction', 'delete_transaction', 'detail_transaction'],
            'quick_add': current_url_name == 'add_transaction',
            
            # Add more sections here e.g. Menu for; drop-down, header-top, mobile float-navigation etc.
            'filter_transactions': (
                current_url_name == 'list_transaction' and 
                transaction_type in ['income', 'expense']
            ),
            'accounts': current_url_name in ['accounts_profile'], # mobile only
        },
        'current_module': None, # Identifies which top-level module is active
        'transaction_filter_type': transaction_type
    }
    
    # Determine current module (for highlighting parent items)
    if context['active_links']['dashboard']:
        context['current_module']='dashboad'
        
    elif context['active_links']['transactions']:
        context['current_module']='transactions'
        
    elif context['active_links']['quick_add']:
        context['current_module']='quick_add' 

    elif context['active_links']['accounts']:
        context['current_module']='accounts'
        
    elif context['active_links']['filter_transactions']:
        context['current_module']='filter_transactions'              
            
    return context            
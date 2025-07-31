def sidebar_context(request):
    current_url_name = request.resolver_match.url_name
    current_url_path = request.path
    
    # Define which URLs belong to which sections
    context = {
        'active_links': {
            'dashboard': current_url_name == 'dashboard',
            'transactions': current_url_name in ['list_transaction', 'edit_tranaction', 'delete_transaction', 'detail_transaction'],
            'quick_add': current_url_name == 'add_transaction',
            # Add more sections here e.g. Drop-down menus
        },
        'current_module': None # Identifies which top-level module is active
    }
    
    # Determine current module (for highlighting parent items)
    if context['active_links']['dashboard']:
        context['current_module']='dashboad'
        
    elif context['active_links']['transactions']:
        context['current_module']='transactions'
        
    elif context['active_links']['quick_add']:
        context['current_module']='quick_add'    
            
    return context            
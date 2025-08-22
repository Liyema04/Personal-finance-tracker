from django.shortcuts import render, redirect
from transactions.forms import UserRegistrationForm, TransactionForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Transaction, Category
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Q
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.core.cache import cache
from django.views.decorators.cache import cache_page
# Lazyload & Pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string
# Filtering
from transactions.filters import TransactionFilter


# Create your views here.
"""
@login_required(login_url="login")
def transactions_login_page(request):
    return redirect("dashboard")
""" 
def transactions_login_page(request):
    error = None
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password1")  # match your form field name
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
            else:
                error = "Invalid username or password. Try again"
                
    return render(request, "accounts/login.html", {"form": {}, "error": error})

def transactions_register_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        form = UserRegistrationForm()
        if request.method == "POST":
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                form.save() # Creates a new user
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user) # Alert displayed on register temp
                return redirect("login") # Redirects to login 
                
    return render(request, "accounts/register.html",{"form": form})

# User-specific profile view 
@login_required(login_url='login')
def user_accounts_profile(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    
    lifetime_totals = transactions.aggregate(
        total_income = Sum('amount', filter=Q(type='income')),
        total_expenses = Sum('amount', filter=Q(type='expense'))
    )
    
    lifetime_income = lifetime_totals['total_income'] or 0
    lifetime_expenses = lifetime_totals['total_expenses'] or 0
    lifetime_balance = lifetime_income - lifetime_expenses
    
    
    context = {
        'transactions': transactions,
        'lifetime_moves': transactions.count(),
        'lifetime_income': float(lifetime_income),
        'lifetime_expenses': float(lifetime_expenses),
        'lifetime_balance': float(lifetime_balance),
    }
    
    return render(request, "accounts/account_profile.html", context)

# User -> logging out 
def transactions_logout_user(request):
    logout(request)
    return redirect('login')

# Transaction CRUD Views

# Add transaction
@login_required(login_url='login')
def transactions_add_transaction_page(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, "New Move added!")
            return redirect("list_transaction")  # Use your URL pattern name here
    else:
        form = TransactionForm()
    return render(request, "transactions/add_transaction.html", {"form": form})

# Edit transaction
@login_required(login_url='login')
def transactions_edit_transaction_page(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user) # (transaction.user = request.user)
    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction.user = request.user
            form.save()
            messages.success(request, 'Move updated.') # Display on list temp 
            return redirect ("list_transaction")
    else:
        form = TransactionForm(instance=transaction) # Pre-update
        return render(request, "transactions/edit_transaction.html", {"form": form, "transaction": transaction})

# Delete Transaction
@login_required(login_url='login')
def transactions_delete_transaction_page(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user) # same as update
    if request.method == "POST":
        transaction.user = request.user
        transaction.delete()
        messages.info(request, 'Move deleted.') # Display on list temp
        return redirect ("list_transaction") # list temp not dashboard
    return render(request, "transactions/confirm_delete.html", {"transaction": transaction})
    
# Each users dashboard view(templates)                 
@login_required(login_url='login')
@cache_page(60*1)
def transactions_user_dashboard(request):
    cache_key = f"dashboard_{request.user.id}"
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return cached_data
    
    # Get date ranges
    today = datetime.now().date()
    thirty_days_ago = today - timedelta(days=30)
    current_month_start = today.replace(day=1)
    
    transactions = Transaction.objects.filter(user=request.user)
    
    # Current Month Moves
    current_month_transactions = transactions.filter(
        date__month = datetime.now().month,
        date__year = datetime.now().year
    ).count()
    
    # Calc totals using Django's aggregate() for better performance
    totals = transactions.aggregate(
        total_income = Sum('amount', filter=Q(type='income')),
        total_expenses = Sum('amount', filter=Q(type='expense')),
        
        # Last 30 days totals (for summary)
        last_30_days_income = Sum('amount', filter=Q(
            type = 'income',
            date__gte=thirty_days_ago
        )),
        last_30_days_expenses = Sum('amount', filter=Q(
            type = 'expense',
            date__gte=thirty_days_ago
        )),
        
        # Current month totals 
        current_month_income = Sum('amount', filter=Q(
            type = 'income',
            date__month = datetime.now().month,
            date__year = datetime.now().year
        )),
        current_month_expenses = Sum('amount', filter=Q(
            type = 'expense',
            date__month = datetime.now().month,
            date__year = datetime.now().year
        ))
    ) 
    
    # Handling values from aggregation - Lifetime (for charts)
    total_income = totals['total_income'] or 0
    total_expenses = totals['total_expenses'] or 0
    
    # Last 30 days (for summary block)
    last_30_days_income = totals['last_30_days_income'] or 0
    last_30_days_expenses = totals['last_30_days_expenses'] or 0
    
    # Current month
    current_month_income = totals['current_month_income'] or 0
    current_month_expenses = totals['current_month_expenses'] or 0
    
    # Monthly totals for line chart  - ensure None values are converted to 0   
    monthly_totals = transactions.annotate(
        month = TruncMonth('date')).values('month').annotate(
            income = Sum('amount', filter=Q(type = 'income')) or 0,
            expense = Sum('amount', filter=Q(type = 'expense')) or 0
        ).order_by('month')
        
    # Convert to list of dictionaries with formatted dates
    monthly_data = []
    for m in monthly_totals:
        month_date = m['month']
        monthly_data.append({
            'month': month_date.strftime('%b %Y'),  # "Jul 2025" format
            'month_sort': month_date.strftime('%Y-%m'),  # For correct ordering
            'income': float(m['income'] or 0),
            'expense': float(m['expense'] or 0)
        })
        
    monthly_data.sort(key=lambda x: x['month_sort'])        
        
    # Category breakdown for  pie/donut chart
    categories = list(transactions.filter(
            date__gte=thirty_days_ago
        ).values('category').annotate(
            total = Sum('amount')
    ).exclude(type='income').order_by('-total')) # Only expenses
    
    for cat in categories:
        cat['total'] = float(cat['total'] or 0)

    context = {
        'monthly_data': json.dumps(monthly_data, cls=DjangoJSONEncoder), # Converted to list for json
        'category_data' : json.dumps(categories, cls=DjangoJSONEncoder),
        'transactions': transactions.order_by('-date')[:5], # Recent 5 
        'total_income': float(total_income), # Lifetime for Charts
        'total_expenses': float(total_expenses), # Lifetime for charts
        'last_30_days_income': float(last_30_days_income), # Last 30 days for summary
        'last_30_days_expenses': float(last_30_days_expenses), # Last 30 days for summary
        'last_30_days_balance': float(last_30_days_income - last_30_days_expenses), # Last 30 days balance
        'current_month_net': float(current_month_income - current_month_expenses),
        'current_month_moves': current_month_transactions,
        'balance': float(total_income - total_expenses) # Lifetime balance
    }
    
    response = render(request, "transactions/dashboard.html", context)
    cache.set(cache_key, response, 60*1)
    return response

# user's list of Transactions (all)
# Adding pagination support


@login_required(login_url='login')
def transactions_list_page(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    
    # Adding pagination support:
    
    # Pagination parameters
    page = request.GET.get('page', 1)
    page_size = int(request.GET.get('page_size', 15)) # Initial load: 15, subsequent: 5
    
    # handling AJAX requests for lazy loading 
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return handle_ajax_transactions(request, transactions)
    
    # For each initial page load, get first 15 transactions
    paginator = Paginator(transactions, 15)
    initial_transactions = paginator.get_page(1) 
    
    
    net_totals = transactions.aggregate(
        net_income = Sum('amount', filter=Q(type='income')),
        net_expenses = Sum('amount', filter=Q(type='expense'))
    )
    
    # Handling values from aggrigation
    net_income = net_totals['net_income'] or 0
    net_expenses = net_totals['net_expenses'] or 0
    net_balance = net_income - net_expenses
    
    context = {
        'transactions': initial_transactions,
        'total_count': transactions.count(),
        'initial_load_count': len(initial_transactions),
        'total_income': float(net_income),
        'total_expenses': float(net_expenses),
        'net_balance': float(net_balance), # Net Balance
        'has_more': initial_transactions.has_next(),
        'current_page': 1,
    }
    return render(request, "transactions/list_transaction.html", context)

# AJAX handler for lazy loading
def handle_ajax_transactions(request, transactions_qs):
    try:
        # prefer offset/limit (client-side uses offset), fall back to page/page_size
        try:
            offset = int(request.GET.get('offset')) if request.GET.get('offset') is not None else None
        except ValueError:
            offset = None

        try:
            limit = int(request.GET.get('limit')) if request.GET.get('limit') is not None else None
        except ValueError:
            limit = None

        if offset is None or limit is None:
            # fallback to page/page_size (1-based page)
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 15))
            offset = (page - 1) * page_size
            limit = page_size

        # ensure same ordering as initial page
        transactions_qs = transactions_qs.order_by('-date')

        start = offset
        end = offset + limit
        page_items = list(transactions_qs[start:end])  # force evaluation

        # Pass request to render_to_string to ensure context processors (e.g. url, static) work
        html = render_to_string('transactions/transaction_rows.html', {'transactions': page_items}, request=request)

        return JsonResponse({
            'success': True,
            'html': html,
            'count': len(page_items),
            'has_more': transactions_qs.count() > end,
            'current_page': (offset // limit) + 1,
            # debug fields to inspect in Network response
            'requested_offset': offset,
            'requested_limit': limit,
            'returned_html_length': len(html)
        })
    except Exception as e:
        # Temporary: return error details for debugging (remove/limit in production)
        import traceback, sys
        tb = traceback.format_exc()
        # Log to server console
        print('AJAX handler error:', tb, file=sys.stderr)
        return JsonResponse({'success': False, 'error': str(e), 'trace': tb}, status=500)

# Shows one transacrion e.g(Most recent in detail !READ-Only!)
@login_required(login_url='login')
def transactions_detail_page(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    
    # Getting human-readable category
    category_display = dict(Category.DEFAULT_CATEGORIES).get(transaction.category) # if error -- try: Category.category
    
    context = {
        'transaction': transaction,
        'category_display': category_display,
        'similar_transactions': Transaction.objects.filter(
            user = request.user,
            category = transaction.category
        ).exclude(id = transaction_id).order_by('-date')[:3] # Suggests related items
    } 
    return render(request, "transactions/detail_transaction.html", context)

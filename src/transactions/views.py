from django.shortcuts import render, redirect
from transactions.forms import UserRegistrationForm, TransactionForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Transaction, Category
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Q
from django.db.models.functions import TruncMonth
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.core.cache import cache
from django.views.decorators.cache import cache_page

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

# User -> logging out 
def transactions_logout_user(request):
    logout(request)
    return redirect('login')

# Transaction CRUD Views
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
    
    transactions = Transaction.objects.filter(user=request.user)
    
    # Calc totals using Django's aggregate() for better performance
    totals = transactions.aggregate(
        total_income = Sum('amount', filter=Q(type='income')),
        total_expenses = Sum('amount', filter=Q(type='expense')),
        
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
    
    #Handling values from aggregation
    total_income = totals['total_income'] or 0
    total_expenses = totals['total_expenses'] or 0
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
    categories = list(transactions.values('category').annotate(
        total = Sum('amount')
    ).exclude(type='income').order_by('-total')) # Only expenses
    
    for cat in categories:
        cat['total'] = float(cat['total'] or 0)

    context = {
        'monthly_data': json.dumps(monthly_data, cls=DjangoJSONEncoder), # Converted to list for json
        'category_data' : json.dumps(categories, cls=DjangoJSONEncoder),
        'transactions': transactions.order_by('-date')[:5], # Recent 5 
        'total_income': float(total_income),
        'total_expenses': float(total_expenses),
        'current_month_net': float(current_month_income - current_month_expenses),
        'balance': float(total_income - total_expenses)
    }
    
    response = render(request, "transactions/dashboard.html", context)
    cache.set(cache_key, response, 60*1)
    return response

# user's list of Transactions (all)
@login_required(login_url='login')
def transactions_list_page(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    
    context = {
        'transactions': transactions,
        'total_count': transactions.count(),
        'total_income': sum(t.amount for t in transactions if t.type == 'income'),
        'total_expences': sum(t.amount for t in transactions if t.type == 'expense'),
    }
    return render(request, "transactions/list_transaction.html", context)

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
    
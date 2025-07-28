from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, TransactionForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Transaction, Category
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Q
from django.db.models.functions import TruncMonth
import json

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
    
                
@login_required(login_url='login')
def transactions_user_dashboard(request):
    #form = TransactionForm()
    
    transactions = Transaction.objects.filter(user=request.user)
    
    # Monthly totals for line chart     
    monthly_totals = transactions.annotate(
        month = TruncMonth('date')).values('month').annotate(
            income = Sum('amount', filter=Q(type = 'income')),
            expense = Sum('amount', filter=Q(type = 'expense'))
        ).order_by('month')
        
    # Category breakdown for  pie/donut chart
    categories = transactions.values('category').annotate(
        total = Sum('amount')
    ).exclude(type='income') # Only expenses

    context = {
        #'form': form,
        'monthly_data': list(monthly_totals), # Convert to list for json
        'category_data' : list(categories),
        'transactions': transactions.order_by('-date')[:5], # Recent 5 
        'total_income': sum(t.amount for t in transactions if t.type == 'income'),
        'total_expences': sum(t.amount for t in transactions if t.type == 'expense'),
    }
    return render(request, "transactions/dashboard.html", context)

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
    
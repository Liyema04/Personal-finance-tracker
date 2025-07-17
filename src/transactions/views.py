from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, TransactionForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
"""
@login_required(login_url="login")
def transactions_login_page(request):
    return redirect("dashboard")
""" 
def transactions_login_page(request):
    error = None
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
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save() # Creates a new user
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user) 
            return redirect("login") # Redirects to login 
    else:
        form = UserRegistrationForm()
    return render(request, "accounts/register.html",{"form": form})

def transactions_add_transaction_page(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect("dashboard")  # Use your URL pattern name here
    else:
        form = TransactionForm()
    return render(request, "transactions/add_transaction.html", {"form": form})

def transactions_user_dashboard(request):
    return render(request, "transactions/dashboard.html")
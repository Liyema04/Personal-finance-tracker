from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Transaction
from bootstrap_datepicker_plus.widgets import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div, HTML
from crispy_forms.bootstrap import InlineRadios

# Our custom User Registration Form (extends Django's built-in UserCreationForm)
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ("first_name", "last_name","username", "email", "password1", "password2")
        labels = {
            "first_name": "Name", 
            "last_name": "Surname", 
            "username": "Username", 
            "email": "Email", 
            "password1": "Password", 
            "password2": "Confirm Password",
        }
        
# Transaction Form (ModelForm for the Transaction model)
class TransactionForm(forms.ModelForm):
    date = forms.DateField(
        widget=DatePickerInput(options={
            "format": "YYYY-MM-DD",
            "showClose": True,
            "showClear": True,
            "showTodayButton": True,             
        })
    )
    
    # Income categories
    INCOME_CATEGORIES = [
        ('SALARY', 'Work/Salary'),
        ('SIDE_HUSTLE', 'Side Hustle'),
        ('BUSARY', 'Scholarship/Bursary'),
        ('ALLOWANCE', 'Family Support'),
        ('STUDENT_LOAN', 'Student Loan'),
        ('GRANT', 'Grant'),
        ('GIFT', 'Gift'), 
    ]
    
    # Expense categories
    EXPENSE_CATEGORIES = [
        ('GROCERIES', 'Groceries'),
        ('RENT', 'Rent/Accommodation'),
        ('TRANSPORT', 'Transport'),
        ('DATA', 'Data/Airtime'),
        ('GYM', 'Gym/Fitness'),
        ('INSURANCE', 'Insurance'),
        ('DEBT', 'Debt Repayment'),
        ('ENTERTAINMENT', 'Entertainment'),
        ('DINING', 'Eating Out'),
        ('EDUCATION', 'Education'),
        ('HEALTH', 'Health/Medical'),
        ('CLOTHING', 'Clothing'),
        ('SAVINGS', 'Savings/Investments'),
        ('SUBSCRIPTIONS', 'Subscriptions'),
        ('PERSONAL_GROOMING', 'Beauty/Grooming'),
    ]
    
    type = forms.ChoiceField(
        choices= Transaction.TRANSACTION_TYPES,
        widget= forms.RadioSelect(attrs={'class': 'type-radio'}),
    )
    
    class Meta:
        model = Transaction
        fields = ("amount", "date", "type", "category", "description")
        labels = {
            "amount": "Amount",
            "date": "Date",
            "type": "Type",
            "category": "Category",
            "description": "Description",
        }
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.RadioSelect(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'})
        }
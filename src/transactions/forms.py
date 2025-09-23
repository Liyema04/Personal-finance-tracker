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
    # Amount field with explicit label
    amount = forms.DecimalField(
        label="Amount",
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter amount'
        })
    )
    
    # Date field with explicit label
    date = forms.DateField(
        label="Date",
        widget=DatePickerInput(options={
            "format": "YYYY-MM-DD",
            "showClose": True,
            "showClear": True,
            "showTodayButton": True,             
        })
    )
    
    # Type field with explicit label
    type = forms.ChoiceField(
        label="Type",
        choices=Transaction.TRANSACTION_TYPES,
        widget=forms.RadioSelect(attrs={
            'class': 'type-radio',
            'onchange': 'updateCategories(this.value)'
        }),
    )
    
    # Category field - we'll populate this dynamically
    category = forms.ChoiceField(
        label="Category",
        choices=[],  # Will be populated by JavaScript
        widget=forms.Select(attrs={
            'class': 'form-control category-select',
            'style': 'display: none;'  # Hidden by default, show buttons instead
        })
    )
    
    # Description field with explicit label
    description = forms.CharField(
        label="Description",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Optional description'
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set initial category choices to all categories
        all_categories = self.INCOME_CATEGORIES + self.EXPENSE_CATEGORIES
        self.fields['category'].choices = [('', 'Select category')] + all_categories
        
        # If we have an instance (editing), set the type-specific categories
        if self.instance and self.instance.pk:
            if self.instance.type == 'income':
                self.fields['category'].choices = [('', 'Select category')] + self.INCOME_CATEGORIES
            else:
                self.fields['category'].choices = [('', 'Select category')] + self.EXPENSE_CATEGORIES
    
    class Meta:
        model = Transaction
        fields = ("amount", "date", "type", "category", "description")
        # Remove labels from here since we're defining them explicitly above
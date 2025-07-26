from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Transaction
from bootstrap_datepicker_plus.widgets import DatePickerInput

# Our custom User Registration Form (extends Django's built-in UserCreationForm)
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        
# Transaction Form (ModelForm for the Transaction model)
class TransactionForm(forms.ModelForm):
    date = forms.DateField(
        widget = DatePickerInput(options={
            "format": "YYYY-MM-DD",
            "showClose": True,
            "showClear": True,
            "showTodayButton": True,             
        })
    )
    
    class Meta:
        model = Transaction
        fields = ["amount", "category", "date", "type", "description"] # Customize fields
        
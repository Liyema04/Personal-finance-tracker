from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    DEFAULT_CATEGORIES = [
        # Income
        ("income", "Work/Salary"),
        ("income", "Side Hustle"),
        ("income", "Scholarship/Bursary"),
        ("income", "Family Support"),
        ("income", "Student Loan"),
        ("income", "Grant"),
        ("income", "Student Loan"),
        # Expense
        ("expense", "Groceries"),
        ("expense", "Rent/Accommodation"),
        ("expense", "Transport"),
        ("expense", "Data/Airtime"),
        ("expense", "Gym/Fitness"),
        ("expense", "Insurance"),
        ("expense", "Debt Repayment"),
        ("expense", "Entertainment"),
        ("expense", "Eating Out"),
        ("expense", "Education"),
        ("expense", "Health/Medical"),
        ("expense", "Clothing"),
        ("expense", "Savings/Investments"),
        ("expense", "Subscriptions"),
    ]
    name = models.CharField(max_length=120,) # max_length = required  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    ) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=22, choices=Category.DEFAULT_CATEGORIES)
    date = models.DateField()
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    description = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return f"{self.type} - {self.amount} on {self.date}"
    
class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    period_start = models.DateField()
    period_end = models.DateField()
    
    def __str__(self):
        return f"{self.category.name} - {self.limit}"     
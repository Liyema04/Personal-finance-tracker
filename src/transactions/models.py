from django.db import models
from django.contrib.auth.models import User
from .managers import TransactionQuerySet

# Create your models here.
class Category(models.Model):
    DEFAULT_CATEGORIES = [
        # Income
        ("SALARY", "Work/Salary"),
        ("SIDE_HUSTLE", "Side Hustle"),
        ("BUSARY", "Scholarship/Bursary"),
        ("ALLOWANCE", "Family Support"),
        ("STUDENT_LOAN", "Student Loan"),
        ("GRANT", "Grant"),
        ("GIFT", "Gift"),
        # Expense
        ("GROCERIES", "Groceries"),
        ("RENT", "Rent/Accommodation"),
        ("TRANSPORT", "Transport"),
        ("DATA", "Data/Airtime"),
        ("GYM", "Gym/Fitness"),
        ("INSURANCE", "Insurance"),
        ("DEBT", "Debt Repayment"),
        ("ENTERTAINMENT", "Entertainment"),
        ("DINING", "Eating Out"),
        ("EDUCATION", "Education"),
        ("HEALTH", "Health/Medical"),
        ("CLOTHING", "Clothing"),
        ("SAVINGS", "Savings/Investments"),
        ("SUBSCRIPTIONS", "Subscriptions"),
        ("PERSONAL_GROOMING", "Beauty/Grooming"),
    ]
    
    """
    BUDGET_CATEGORIES = [
        # Expenditure
        ("GROCERIES", "Groceries"),
        ("RENT", "Rent/Accommodation"),
        ("TRANSPORT", "Transport"),
        ("DATA", "Data/Airtime"),
        ("GYM", "Gym/Fitness"),
        ("INSURANCE", "Insurance"),
        ("DEBT", "Debt Repayment"),
        ("ENTERTAINMENT", "Entertainment"),
        ("DINING", "Eating Out"),
        ("EDUCATION", "Education"),
        ("HEALTH", "Health/Medical"),
        ("CLOTHING", "Clothing"),
        ("SAVINGS", "Savings/Investments"),
        ("SUBSCRIPTIONS", "Subscriptions"),
        ("PERSONAL_GROOMING", "Beauty/Grooming")
    ] 
    """
    
    name = models.CharField(max_length=120,) # max_length = required  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    category = models.CharField(
        max_length=50,
        choices=DEFAULT_CATEGORIES,
        default='SALARY'
    )
    """
    budget_category = models.CharField(
        max_length=50,
        choices=BUDGET_CATEGORIES,
        default='ENTERTAINMENT'
    )
    """
    # Getting expenditure categories for budget
    def get_expense_categories():
        income_keys = {"SALARY", "SIDE_HUSTLE", "BUSARY", "ALLOWANCE", "STUDENT_LOAN", "GRANT", "GIFT"}
        return [choice for choice in Category.DEFAULT_CATEGORIES if choice[0] not in income_keys]
    
    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    ) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=22, choices=Category.DEFAULT_CATEGORIES) # preset categories in form
    date = models.DateField()
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    description = models.CharField(max_length=255, blank=True)
    
    objects = TransactionQuerySet.as_manager()
    
    def __str__(self):
        return f"{self.type} - {self.amount} on {self.date}"
    
class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    
    # store category code/string as plain text in DB;
    # choices will be provided at form time (so user-created categories are included)
    category = models.CharField(max_length=50) # set budget categories in form
    
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    
    period_start = models.DateField()
    
    period_end = models.DateField()
    
    def __str__(self):
        # category is stored as string; show that value
        return f"{self.category} - {self.limit}"     
from django.db import models
from django.contrib.auth.models import User

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
    ]
    name = models.CharField(max_length=120,) # max_length = required  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    category = models.CharField(
        max_length=50,
        choices=DEFAULT_CATEGORIES,
        default='SALARY'
    )
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
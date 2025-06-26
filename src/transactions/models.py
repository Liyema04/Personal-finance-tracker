from django.db import models

# Create your models here.
class Transaction(models.Model):
    user = models.TextField()
    amount = models.TextField()
    category = models.TextField()
    date = models.TextField()
    type = models.TextField()
    
class Budget(models.Model):
    user = models.TextField()
    category = models.TextField()
    limit = models.TextField()     
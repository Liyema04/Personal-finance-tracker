from django.contrib import admin
from .models import Transaction # relative import
from .models import Budget
from .models import Category

# Register your models here.
admin.site.register(Transaction)
admin.site.register(Budget)
admin.site.register(Category)
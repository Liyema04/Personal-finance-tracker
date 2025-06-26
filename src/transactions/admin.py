from django.contrib import admin
from .models import Transaction # relative import
from .models import Budget

# Register your models here.
admin.site.register(Transaction)
admin.site.register(Budget)
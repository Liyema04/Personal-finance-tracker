# Factories.py Fixes and Corrections

## Issues Found

### 1. **Incorrect User Import**
**Issue**: User is imported from `transactions.models`, but it should be from Django's auth models.
```python
# ❌ Current (Incorrect)
from transactions.models import Transaction, Category, User

# ✅ Correct
from django.contrib.auth.models import User
from transactions.models import Transaction, Category
```

---

### 2. **CategoryFactory Missing Required Fields**
**Issue**: The `Category` model requires both `user` (ForeignKey) and `category` (CharField with choices), but the factory only provides `name`.

**Model Definition**:
```python
class Category(models.Model):
    name = models.CharField(max_length=120)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    category = models.CharField(max_length=50, choices=DEFAULT_CATEGORIES, default='SALARY')
```

**Current Factory**:
```python
# ❌ Incorrect - Missing user and category fields
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ('name',)
    
    name = factory.Iterator(['Side Hustle', 'Work/Salary', 'Rent/Accommodation', 'Groceries', 'Entertainment'])
```

**Corrected Factory**:
```python
# ✅ Correct - Includes all required fields
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    
    user = factory.SubFactory(UserFactory)
    name = factory.Faker('word')
    category = factory.Faker(
        'random_element',
        elements=[x[0] for x in Category.DEFAULT_CATEGORIES]
    )
```

---

### 3. **TransactionFactory Has Wrong Category Field**
**Issue**: The `Transaction` model stores `category` as a CharField (the category code), not as a ForeignKey to Category model. The factory incorrectly uses SubFactory.

**Model Definition**:
```python
class Transaction(models.Model):
    category = models.CharField(max_length=22, choices=Category.DEFAULT_CATEGORIES)
```

**Current Factory**:
```python
# ❌ Incorrect - Treats category as ForeignKey
category = factory.SubFactory(CategoryFactory)
```

**Corrected Factory**:
```python
# ✅ Correct - Passes category code as string
category = factory.Faker(
    'random_element',
    elements=[x[0] for x in Category.DEFAULT_CATEGORIES]
)
```

---

### 4. **Hard-Coded Amount in TransactionFactory**
**Issue**: The amount is hard-coded to `565`, which doesn't create realistic test data variation.

**Current**:
```python
# ❌ Hard-coded
amount = 565
```

**Corrected**:
```python
# ✅ Random decimal values
amount = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
```

---

## Corrected Complete factories.py

```python
from datetime import datetime
import factory
from django.contrib.auth.models import User
from transactions.models import Transaction, Category


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Sequence(lambda n: 'user%d' % n)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    user = factory.SubFactory(UserFactory)
    name = factory.Faker('word')
    category = factory.Faker(
        'random_element',
        elements=[x[0] for x in Category.DEFAULT_CATEGORIES]
    )


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    user = factory.SubFactory(UserFactory)
    category = factory.Faker(
        'random_element',
        elements=[x[0] for x in Transaction.TRANSACTION_TYPES[0][0] for x in Category.DEFAULT_CATEGORIES]
    )
    amount = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    date = factory.Faker(
        'date_between',
        start_date=datetime(year=2025, month=11, day=1).date(),
        end_date=datetime.now().date()
    )
    type = factory.Faker(
        'random_element',
        elements=[x[0] for x in Transaction.TRANSACTION_TYPES]
    )
```

---

## Summary of Changes

| Issue | Fix |
|-------|-----|
| User import source | Move to `django.contrib.auth.models` |
| CategoryFactory fields | Add `user` (SubFactory) and `category` (random choice) |
| TransactionFactory category | Change from SubFactory to string choice |
| TransactionFactory amount | Randomize instead of hard-coding to 565 |


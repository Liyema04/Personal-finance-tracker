"""
URL configuration for finance_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from landing_page.views import landing_page_welcome, default, landing_page_about, landing_page_contact
from transactions.views import (
    transactions_login_page,
    transactions_logout_user, 
    transactions_register_page,
    # CRUD - views.py
    transactions_add_transaction_page,
    # not implemented
    transactions_list_page,
    transactions_detail_page,
    transactions_edit_transaction_page,
    transactions_delete_transaction_page,
    # dash - views.py
    transactions_user_dashboard,
    user_accounts_profile,
    logo_svg,     
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # landing_page(component) - urls
    path('', default, name='default'),
    path('welcome/', landing_page_welcome, name='welcome'), # welcome/(landing page)
    path('about/', landing_page_about, name='about'),
    path('contact/', landing_page_contact, name='contact'),
    
    # transactions(component) - urls
    
    # Register & Login/Logout 
    path('login/', transactions_login_page, name='login'),
    path('logout', transactions_logout_user, name='logout'),
    path('register/', transactions_register_page, name='register'),
    
    # Rendering logo
    path('logo.svg', logo_svg, name='logo_svg'),
    
    # User Account
    path('accounts/profile', user_accounts_profile, name ='accounts_profile'),
    
    # Transaction CRUD (grouped under /transactions)
    path('transactions/list/', transactions_list_page, name='list_transaction'), # Read: list all
    path('transactions/<int:transaction_id>/', transactions_detail_page, name='detail_transaction'), #Read: detail
    path('transactions/add/', transactions_add_transaction_page, name='add_transaction'), # Create/ Add - (new)
    path('transactions/<int:transaction_id>/edit/', transactions_edit_transaction_page, name='edit_transaction'), # Update
    path('transactions/<int:transaction_id>/delete', transactions_delete_transaction_page, name='delete_transaction'), # Delete
    
    # visualise spending data
    path('dashboard', transactions_user_dashboard, name='dashboard'),
    
     
    
    # admin 
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

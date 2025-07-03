from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def default(request, *args, **kwargs):
    return HttpResponse("<h1>Default</h1>") 

def landing_page_welcome(request, *args, **kwargs): # *args & **kwargs - Python basics
    # return HttpResponse("<h1>Welcome to SentiWise</h1>") # string of HTML code not template 
    return render(request, "home(base).html",{})

def landing_page_about(request, *args, **kwargs):
    return render(request, "about.html", {})

def landing_page_contact(request, *args, **kwargs):
    return render(request, "contact.html", {})
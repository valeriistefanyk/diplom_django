from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def show_something(request):
    return HttpResponse('SOMETHING INFO')
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def management(request):
    return HttpResponse('<h2>Management</h2>')
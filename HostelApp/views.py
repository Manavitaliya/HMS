from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index1(request):
    return HttpResponse("hELLO wORLD")


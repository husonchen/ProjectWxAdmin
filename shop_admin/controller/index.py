from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

def hello(request):
    return render(request, 'index.html', {})
from django.http import HttpResponse
from django.http import HttpResponseRedirect

def hello(request):
    return HttpResponseRedirect('/dashboard/')
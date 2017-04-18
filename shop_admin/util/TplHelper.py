from django.template import Context, loader
from django.http import HttpResponse
from django.conf import settings

def getTpl(context,template):
    t = loader.get_template(template+'.html')
    return HttpResponse(t.render(context))
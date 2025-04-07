from django.template import loader
from django.http import HttpResponse

def portal(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())
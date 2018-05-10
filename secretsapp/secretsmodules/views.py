from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse('Hello World')

# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        my_dict = {'inserted_stuff':'testing'}
        return render(request, 'secretmodules/index.html', context=my_dict)

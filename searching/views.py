from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from searching.forms import TeamnameSearchForm

class Base(View):
    
    def get(self, request):
        return render(request, 'base.html')

class Index(View):

    def get(self, request):
        form = TeamnameSearchForm()
        return render(request, 'index.html', {'form': form})


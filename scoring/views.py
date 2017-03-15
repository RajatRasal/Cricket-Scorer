from django.shortcuts import render
from django.views.generic import View


class ScoringInterface(View):

    def get(self, request):
        '''
        This get method is being inherited by the MatchDetails class in the
        views.py file in the searching application folder.
        '''
        print('SCORING INTERFACE CLASS')
        return render(request, 'scoring.html')

    def post(self, request):
        '''
        This post method is being overriden when inherited by the MatchDetails
        class in the views.py file in the searching application folder.
        '''

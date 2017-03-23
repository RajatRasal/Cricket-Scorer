import json

from django.views.generic import View
from django.db import connection
from django.shortcuts import render, HttpResponse

from .models import BallByBall


class ScoringInterface(View):
    def __init__(self):
        self.render_file = "scoring.html"
        self.cursor = connection.cursor()

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

        print('arrived here with no issue')
        print(request.POST)
        self.cursor.execute("""PRAGMA table_info(scoring_ballbyball)""")
        column_names = list(map(lambda x: x[1], list(self.cursor.fetchall())))
        self.cursor.execute("""SELECT * FROM scoring_ballbyball
                            ORDER BY id DESC LIMIT 1""")
        last_ball = list(self.cursor.fetchone())
        context = dict(zip(column_names, last_ball))
        return HttpResponse(json.dumps(context),
                            content_type="application/json")

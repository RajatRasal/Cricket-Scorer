import json

from django.views.generic import View
from django.shortcuts import (render,
                              HttpResponse,
                              render_to_response,)
from django.template.loader import render_to_string
from django.template import Context

from .algorithms import DatabaseStackImplementation, Queries


class ScoringInterface(View, DatabaseStackImplementation):

    def __init__(self):
        super(ScoringInterface, self).__init__()
        print('++++++++++++++++++++++++++++++++++++++++++')
        try:
            print('INITALISING')
            self.player_selection_file = "scoring_player_selection.html"
            self.player_live_stats_file = "scoring_live_stats_players_row.html"
            self.ballbyball_live_stats_file = "scoring_last_10_balls.html"
            self.database_stack = DatabaseStackImplementation()
            self.last_ball = self.database_stack.peek()
            # print(self.last_ball)
            self.database_query = Queries()
        except TypeError:
            print('''Scoring Interface is being initialised from another view
                  so we can ignore this part''')

    def get(self, request):
        '''
        This get method is being inherited by the MatchDetails class in the
        views.py file in the searching application folder.

        accessing queries class
        '''

        print('GET')

        try:
            print('request: {}'.format(request.GET['data']))
            request_status_from_scoring_page = request.GET['data']

            if request_status_from_scoring_page == 'onstrike':
                context = Context({
                    'title': 'select onstrike',
                    'query': self.database_query.get_all_available_batters(),
                    'fieldname': request_status_from_scoring_page})
                return_str = render_to_string(self.player_selection_file, context)

            elif request_status_from_scoring_page == 'offstrike':
                context = Context({
                    'title': 'select offstrike',
                    'query': self.database_query.get_all_available_batters(),
                    'fieldname': request_status_from_scoring_page})
                return_str = render_to_string(self.player_selection_file, context)

            elif request_status_from_scoring_page == 'bowler':
                print(self.database_query.get_all_available_bowlers())
                context = Context({
                    'title': 'select bowler',
                    'query': self.database_query.get_all_available_bowlers(),
                    'fieldname': request_status_from_scoring_page})
                return_str = render_to_string(self.player_selection_file, context)

            elif request_status_from_scoring_page == 'live_stats':
                print('LIVE STATS REQUEST')
                onstrike = self.last_ball['onstrike']
                print('ONSTRIKE:',onstrike)
                onstrike_context = self.database_query.get_live_batter_stats(onstrike)
                offstrike = self.last_ball['offstrike']
                print('OFFSTRIKE:',offstrike)
                offstrike_context = self.database_query.get_live_batter_stats(offstrike)
                bowler = self.last_ball['bowler']
                print('BOWLER:',bowler)
                offstrike_context = self.database_query.get_live_batter_stats(offstrike)
                bowler_context = self.database_query.get_live_bowler_stats(bowler)
                ball_by_ball_context = Context({
                    'last_10': self.database_query.get_last_ten_balls()})

                return_str = {'onstrike':
                               render_to_string(self.player_live_stats_file, onstrike_context),
                               'offstrike':
                               render_to_string(self.player_live_stats_file, offstrike_context),
                               'bowler':
                               render_to_string(self.player_live_stats_file, bowler_context),
                              'last_10':
                              render_to_string(self.ballbyball_live_stats_file, ball_by_ball_context)
                               }

            print('return_str: ', return_str)
            return HttpResponse(json.dumps(return_str),
                                content_type="application/json")
        except Exception as e:
            print(e)
            # initial condition where request data = {} = empty key-value list
            print('initial get')
            return render(request, "scoring.html")
        # return_str = json.dumps(self.database_stack.peek())
        # return render(self.render_file, {"initial_data":return_str})

    def post(self, request):
        '''
        This post method is being overriden when inherited by the MatchDetails
        class in the views.py file in the searching application folder.
        url(r'^get_scores/$', csrf_exempt(ScoringInterface.as_view())),

        accessing db stack class
        '''
        print(dict(request.POST))
        if request.is_ajax():
            if request.POST == {}:
                # initial condition
                print('initial post')
                return_str = json.dumps(self.database_stack.peek())
            else:
                ball = dict(request.POST)
                ball.update((x, y[0]) for x, y in ball.items())
                if request.POST.get('people_involved') == 'UNDO':
                    print('undo -----------------------------------')
                    return_str = json.dumps(self.database_stack.pop(ball))
                else:
                    # Puts the returned response in the required format for the push
                    # method onto the database implemented as a stack.
                    # Currently each key is mapped to a single index array,
                    # but the below line will map each key to a single element.
                    print('dont undo++++++++++++++++++++++++++++++++')
                    print(ball)
                    self.database_stack.push(ball)
                    return_str = json.dumps(self.database_stack.peek())
        print('return_str:', return_str)
        return HttpResponse(return_str, content_type="application/json")

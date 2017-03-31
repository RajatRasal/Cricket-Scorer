"""
THIS FILE CONTAINS ALL THE VIEW FUNCTIONS.

When a  request is made to the server on a particular URL path, the code in the urls.py
file will map that request to a view function in this file.

The view function will determine whether the request made to it was a GET or a
POST. Then depending on this, it either call its GET or POST methods and pass to them
the ontents of the request being made.

The GET or POST methods can called automatically once the request is determined to be
a GET or POST request because the view functions in this file are all children of
the View class, since they are all inheriting View. View is a class provided by the
standard django library.
"""

import json

from django.views.generic import View
from django.shortcuts import render, HttpResponse
from django.template.loader import render_to_string
from django.template import Context

from .algorithms import DatabaseStackImplementation, Queries


class ScoringInterface(View):
    """
    Looking at the urls.py file - when a GET request is made to
    http://localhost:PORT/scoring_submit/, the get function in this class will be called,
    AND when a POST request is made to the same URL, the post function in this class
    will be called.

    Data from the GET or POST request is passed into the 'request' parameter of the
    get or post function.
    """

    def __init__(self):
        super(ScoringInterface, self).__init__()
        try:
            self.player_selection_file = "scoring_player_selection.html"
            self.player_live_stats_file = "scoring_live_stats_players_row.html"
            self.ballbyball_live_stats_file = "scoring_last_10_balls.html"
            self.database_stack = DatabaseStackImplementation()

            # retrieving data from the last ball that has happened, thus retrieving data
            # from the top of the database stack implementation
            self.last_ball = self.database_stack.peek()
            self.database_query = Queries()
        except TypeError:
            print('''Scoring Interface is being initialised from another view
            so we can ignore this part''')

        def get(self, request):
            '''
            This get method is being inherited by the MatchDetails class in the
            views.py file in the searching application folder.
            '''

            try:
                # extracting the data from the GET request
                request_status_from_scoring_page = request.GET['data']

                if request_status_from_scoring_page == 'onstrike':
                    # Creates a format which can be passed into the html Django template
                    # such that is can be manipulated by the template language tags.
                    context = Context({
                        'title': 'select onstrike',
                        'query': self.database_query.get_all_available_batters(),
                        'fieldname': request_status_from_scoring_page})
                    # Makes the data put in the displayable in the main HTML page by passing
                    # it into a template file 'scoring_player_selection.html'.
                    # The dynamically produced HTML is then converted to a string.
                    return_str = render_to_string(self.player_selection_file, context)

                elif request_status_from_scoring_page == 'offstrike':
                    # Creates a format which can be passed into the html Django template
                    # such that is can be manipulated by the template language tags.
                    context = Context({
                        'title': 'select offstrike',
                        'query': self.database_query.get_all_available_batters(),
                        'fieldname': request_status_from_scoring_page})
                    # Makes the data put in the displayable in the main HTML page by passing
		            # it into a template file 'scoring_player_selection.html'.
		            # The dynamically produced HTML is then converted to a string.
                    return_str = render_to_string(self.player_selection_file, context)

                elif request_status_from_scoring_page == 'bowler':
	                # Creates a format which can be passed into the html Django template
	                # such that is can be manipulated by the template language tags.
context = Context({
'title': 'select bowler',
'query': self.database_query.get_all_available_bowlers(),
'fieldname': request_status_from_scoring_page})
# Makes the data put in the displayable in the main HTML page by passing
		# it into a template file 'scoring_player_selection.html'.
		# The dynamically produced HTML is then converted to a string.
return_str = render_to_string(self.player_selection_file, context)

elif request_status_from_scoring_page == 'live_stats':
	# retrieve data from the top record in the database stack implementation
	# retrieve data from the events of the last ball
onstrike = self.last_ball['onstrike']
onstrike_context = self.database_query.get_live_batter_stats(onstrike)
offstrike = self.last_ball['offstrike']
offstrike_context = self.database_query.get_live_batter_stats(offstrike)
bowler = self.last_ball['bowler']
offstrike_context = self.database_query.get_live_batter_stats(offstrike)
bowler_context = self.database_query.get_live_bowler_stats(bowler)

	# Creates a format which can be passed into the html Django template
	# such that is can be manipulated by the template language tags.
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

# Returns data in Json format to the client side by converting all the
# return_str key-value store to a JSON object using json.dumps().
return HttpResponse(json.dumps(return_str),
content_type="application/json")
except Exception as e:
# initial condition where request data = {} = empty key-value list
# just returns the main scoring interface page
return render(request, "scoring.html")


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
                # creates a JSON object to be returned to the client side containing
                # all the data that has happened during the first ball in the db stack
                return_str = json.dumps(self.database_stack.peek())
            else:
                ball = dict(request.POST)
                ball.update((x, y[0]) for x, y in ball.items())
                if request.POST.get('people_involved') == 'UNDO':
                    return_str = json.dumps(self.database_stack.pop(ball))
                else:
                    # Puts the returned response in the required format for the push
                    # method onto the database implemented as a stack.
                    # Currently each key is mapped to a single index array,
                    # but the below line will map each key to a single element.
                    self.database_stack.push(ball)
                    return_str = json.dumps(self.database_stack.peek())
        return HttpResponse(return_str, content_type="application/json")

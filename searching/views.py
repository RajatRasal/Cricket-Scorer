import json
from re import sub

from django.shortcuts import render, HttpResponse
from django.views.generic import View
from django.template import Context
from django.template.loader import render_to_string
from django.db import connection

from searching.models import Team
from searching.forms import (TeamnameSearchForm,
                             MatchDetailsForm,
                             GeneralTextForm,
                             AjaxTestForm,
                             )
from scoring.views import ScoringInterface


class Base(View):
    """
    The View is being inherited from the methods and classes provided by Django
    and will allow the get and post methods in this class to be called up when
    a get or post is made on the page when this class is being used to produce
    HTML.
    """

    def get(self, request):
        return render(request, 'base.html')


class Index(View):

    def get(self, request):
        # The specific 'class_name' and 'id' arguments should be
        # placed in the constructor, however since these will
        # only be called once in

        # POSSIBLY ADD ALL THE CLASS_NAME AND ID TO THE __INIT__
        # AND THEN INHERIT THIS IN ALL THE OTHER VIEWS !!!!
        hidden_text_input = GeneralTextForm(
                class_name="home-team",
                id="hidden-input")
        teamname_search_form = TeamnameSearchForm(
                placeholder="Enter Team Name",
                id="team-name-search")
        playername_search_form = TeamnameSearchForm(
                placeholder="Enter Player Name",
                id="player-name-search")
        match_details_form = MatchDetailsForm()
        print('hidden text field: %s' % (str(hidden_text_input)))

        return render(request, 'index.html',
                      {'team_name_form': teamname_search_form,
                       'match_details_form': match_details_form,
                       'hidden_text_input_form': hidden_text_input,
                       'player_name_form': playername_search_form, }
                      )


class TeamSearch(View):

    def __init__(self):
        self.cursor = connection.cursor()
        self.data_name = 'names'
        self.data = ''
        self.render_file = 'search_results.html'
        # properties below will be used to construct the sql query
        self.table_name = 'searching_team'
        self.column_name = 'team_name'
        # form properties
        self.placeholder = "Enter Team Name"
        self.id = "team-name-search"

    def post(self, request):
        print('Team Search POST')
        print('REQUEST', request)
        print('REQUEST', request.POST)
        form = TeamnameSearchForm(request.POST,
                                  placeholder=self.placeholder, id=self.id)
        print(form)

        if form.is_valid():  # Add my own validation here
            print('INPUT IS VALID')

            # ADD SOME VALIDATION TO CHECK IF THE TEAM NAME ENTERED IS ALREADY
            # IN THE DATABASE UNDER THE CURRENT MATCH. IF SO, MOVE TO THE ELSE
            # STATEMENT SO NO NAMES ARE RETURNED.
            # Add this in testing, where we make sure that this is not possible

            # takes the searched for text from the POSt request and 'cleans' it
            query = form.cleaned_data['query']
            print('cleaned input/query: {}'.format(query))
            print(type(query))

            # Querying the db with a command akin to like SQL statement
            # (read the doc for details about __icontains) converted to list
            # in order to convert from db object to an iterable
            # form is vulnerable to injection here !!!!!
            # CREATE 2 TESTS
            print("""QUERY: SELECT %s FROM %s WHERE %s LIKE '%s%s%s';""" %
                  (self.column_name, self.table_name,
                   self.column_name, '%', query, '%'))
            # unsafe query
            self.cursor.execute(
                """SELECT %s FROM %s
                    WHERE %s LIKE '%s%s%s';""" %
                (self.column_name, self.table_name,
                 self.column_name, '%', query, '%'))
            # safe query, has no semicolon, so python parameterises everything
            # self.cursor.execute("""SELECT team_name FROM searching_team
            #         WHERE team_name LIKE '%s%s%s'""" % ('%',query,'%'))

            self.data = list(map(lambda z: z[0], self.cursor.fetchall()))
            print(self.data)
            # team_names = list(Team.objects.filter(team_name__icontains=query))

            # creates a format which can be passed into the html
            context = Context({'query': query, self.data_name: self.data})
            print('context: {}'.format(context))

            # Adds the context to the correct place on the page, by passing into
            # a separate mini html file 'search_results.html'.
            return_str = render_to_string(self.render_file, context)
            print('returned string: {}'.format(return_str))

            # Returns the mini html page as a JSON response to be displayed
            # in the search results on the index.html page.
            print("=================================================")
            return HttpResponse(
                json.dumps(return_str),
                content_type="application/json")

        else:
            return HttpResponse(json.dumps(""), content_type="application/json")


class PlayerSearch(TeamSearch):
    """
    Class inherits from TeamSearch but has different values
    of some of the properties. This is because once the 'post' function
    for this subclass is triggered when a POST request is made to
    'host/player_search/', the parts of the db that are queried and the
    the html elements which are returned should be separate for player
    and team name searches.
    """

    def __init__(self):
        # Inherits all the properties from the parent super class which in this
        # case is TeamSearch. Some of the properties will be redefined and
        # other which are not redefined below will remain the same.
        # Initialising the parent class
        super().__init__()
        # properties below will be used to construct the sql query
        self.table_name = 'searching_player'
        self.column_name = 'player_name'
        # form properties
        self.placeholder = 'Enter player name'
        self.id = 'player-name-search'


class TeamSelection(View):

    def post(self, request):
        print('Team Selection POST')
        # form = GeneralTextForm(request.POST)
        form = request.POST
        print('REQUEST.POST', form)

        team_name = str(dict(request.POST)['general_input'][0])
        print('TEAM NAME', team_name)

        cursor = connection.cursor()
        print("""QUERY: SELECT player_name FROM searching_player
        WHERE current_team_name_id=(SELECT id FROM searching_team
        WHERE team_name=%s);""" % (team_name))
        cursor.execute("""SELECT player_name FROM searching_player
        WHERE current_team_name_id=(
        SELECT id FROM searching_team WHERE team_name=%s);""", [team_name])
        # fetchall returns query results in the format:
        # [('player 1',), ('player2',), ('player3',),...
        # This is not desirable when being displayed, so the map functions
        # maps each tuple in the query results list to being just the player
        # name string, to make the output look like this:
        # ['player 1', 'player 2', 'player 3'...]
        # The output of the 'map' is returned as a 'map' object, so needs
        # to be converted to a list.
        player_names = list(map(lambda z: z[0], cursor.fetchall()))
        print(player_names)

        # creates a format which can be passed into the html
        context = Context({'player_names': player_names})
        print('context: {}'.format(context))

        # Adds the context to the correct place on the page, by passing into a
        # separate mini html file 'team_player_results.html'.
        return_str = render_to_string('team_player_results.html', context)
        print('returned string: {}'.format(return_str))

        return HttpResponse(
            json.dumps(return_str),
            content_type="application/json")


class Statistics(View):

    def __init__(self):
        self.cursor = connection.cursor()
        # properties below will be used to construct the sql query
        self.table = ""
        self.column_name = ""
        self.column_names = ""

    def post(self, request):
        print('STATS POST')
        print('REQUEST POST:', request.POST)
        form = GeneralTextForm(request.POST, class_name="", id="hidden-input")
        print(form)
        print(self.table)

        name = str(dict(request.POST)['general_input'][0])

        print("""QUERY: SELECT * FROM %s
        WHERE %s='%s'""" % (self.table, self.column_name, name))
        self.cursor.execute("""SELECT * FROM %s
        WHERE %s='%s'""" % (self.table, self.column_name, name))
        # fetchall returns query results for one column in the format:
        # [(col1, col2, col3, col4,)] <-- single tuple with in list
        # So we can access the all this data in an iterable format, one
        # column at a time, we take the 0th index of the returned list to
        # access the tuple.
        stats = [[a, b] for a, b in zip(self.column_names,
                                        self.cursor.fetchall()[0]) if b != name]
        print(stats)

        # creates a format which can be passed into the html
        context = Context({'name': name, 'statistics': stats})
        print('context: {}'.format(context))

        # Adds the context to the correct place on the page, by passing
        # into a separate mini html file 'team_player_results.html'.
        return_str = render_to_string('statistics.html', context)
        print('returned string: {}'.format(return_str))

        return HttpResponse(
            json.dumps(return_str),
            content_type="application/json")


class PlayerStatistics(Statistics):

    def __init__(self):
        super().__init__()
        self.table = "searching_player"
        self.column_name = "player_name"
        # returns a list of all the column names
        self.column_names = self.cursor.execute("""
                PRAGMA table_info('%s')""" % (self.table)).fetchall()
        # Add regex to remove the underscores in the column names and replace
        # with spaces. Example of Python FUNCTIONAL PROGRAMMING.
        self.column_names = list(map(lambda z: sub('_', ' ', str(z[1])),
                                     self.column_names))
        # Remove any column names which have the term 'id' in them.
        # Example of Python FUNCTIONAL PROGRAMMING.
        self.column_names = list(filter(lambda z: 'id' not in z,
                                        self.column_names))
        print(self.column_names)


class TeamStatistics(Statistics):

    def __init__(self):
        # complete this properly once the scoring system is complete.
        super().__init__()
        self.table = "searching_match_details"
        self.column_name = ""


class MatchDetails(ScoringInterface):
    """
    View does not need to be inherited here since it is being inherited through
    the ScoringInterface class. The ScoringInterface class inherits View, so
    it does not need to be menitoned here again.
    """

    def __init__(self):
        super().__init__()
        self.cursor = connection.cursor()
    # possibly use inheritance here to get the GET function from the
    # file in the scoring folder?????
    # send any posting requests to that file

    # def get(self, request):
        # print('MATCH DETAILS GET')
        # return render(request, 'base.html')

    def post(self, request):
        print('MATCH DETAILS POST')

        print(type(request.POST))
        match_details = dict(request.POST)
        print('MATCH DETAILS DICTIONARY SUBMISSION: {}'.format(match_details))
        # team_id_get = "SELECT * FROM searching_team WHERE team_name = %s
        # home_team_id = Team.objects
        if match_details['ground_location'] == 'home':
            self.cursor.execute("""SELECT home_ground FROM searching_team
                                WHERE id=%s;""" %
                                (int(match_details['home_team'][0])))
        else:
            self.cursor.execute("""SELECT home_ground FROM searching_team
                                WHERE id=%s;""" %
                                (int(match_details['away_team'][0])))
        match_details['ground_location'] = self.cursor.fetchone()[0]
        print('MATCH DETAILS DICTIONARY ALTERNATION: {}'.format(match_details))

        print(match_details['ground_location'],
              match_details['umpire_1'][0],
              match_details['umpire_2'][0],
              match_details['weather'][0],
              match_details['away_team'],
              match_details['home_team'],
              match_details['batting_first'][0],
              match_details['overs'])

        self.cursor.execute("""INSERT INTO searching_match
                            (date, ground_location, umpire_1, umpire_2, weather,
                            away_team_id, home_team_id, batting_first, overs)
                            VALUES (DATE('now'), '%s', '%s', '%s', '%s',
                            %s, %s, '%s', %s)""" % (match_details['ground_location'],
                                                    match_details['umpire_1'][0],
                                                    match_details['umpire_2'][0],
                                                    match_details['weather'][0],
                                                    int(match_details['away_team'][0]),
                                                    int(match_details['home_team'][0]),
                                                    match_details['batting_first'][0],
                                                    int(match_details['overs'][0])))
        return HttpResponseRedirect("/scoring/")
        #return render(request, 'scoring.html')

class AjaxTest(View):

    def get(self, request):
        form = AjaxTestForm()
        params = dict()
        params["search"] = form
        print('GET VALID')
        return render(request, 'ajax_test.html', params)

    def post(self, request):
        print('POST VALID')
        form = AjaxTestForm(request.POST)

        if form.is_valid():
            # check POC for comment details
            print('SEARCH IS VALID')

            # takes the searched for text from the POST request
            query = form.cleaned_data['query']
            print('query: {}'.format(query))

            team_names = list(Team.objects.filter(team_name__icontains=query))

            # creates a format which can be passed into into the html
            context = Context({"query": query, "team_names": team_names})
            print('context: {}'.format(context))

            # Adds the context to the correct place in the
            return_str = render_to_string('search_results.html', context)
            print('return str: {}'.format(return_str))

            return HttpResponse(json.dumps(return_str),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps(""), content_type="application/json")


if __name__ == "__main__":
    print('hi')
    print(TeamnameSearchForm)

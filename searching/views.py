import json
from re import sub

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.template import Context
from django.template.loader import render_to_string
from django.db import connection

from searching.models import Team
from searching.forms import TeamnameSearchForm, MatchDetailsForm, GeneralTextForm
from searching.algorithms import merge_sort
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
        # SQL into which a parameter can be passed
        self.sql = 'SELECT team_name FROM searching_team WHERE team_name LIKE %s'
        # form properties
        self.placeholder = "Enter Team Name"
        self.id = "team-name-search"

    def post(self, request):
        form = TeamnameSearchForm(request.POST,
                                  placeholder=self.placeholder, id=self.id)

        if form.is_valid():  # Add my own validation here
            # takes the searched for text from the POSt request and 'cleans' it
            query = form.cleaned_data['query']

            # CREATE 2 TESTS
            # print("""QUERY: SELECT %s FROM %s WHERE %s LIKE '%s%s%s';""" %
            # (self.column_name, self.table_name,
            # self.column_name, '%', query, '%'))
            # print('QUERY: ', end='')
            # print(self.sql % (query+'%'))
            # unsafe query
            # self.cursor.execute("""SELECT %s FROM %s WHERE %s LIKE '%s%s%s';"""
            #                    % (self.column_name, self.table_name,
            #                       self.column_name, '%', query, '%'))
            # safe query, has no semicolon, so python parameterises everything
            self.cursor.execute(self.sql, ['%'+query+'%'])

            self.data = list(map(lambda z: z[0], self.cursor.fetchall()))
            self.data = merge_sort(self.data)

            # creates a format which can be passed into the html
            # CAN I MERGE THE PLAYERSEARCH AND TEAMSELECTION ONLY DIFFERENCE
            # IS THAT CONTEXT INCLUDES QUERY IS TJAT NECESARY??????????????????
            context = Context({'query': query, self.data_name: self.data})
            # print('context: {}'.format(context))

            # Adds the context to the correct place on the page, by passing into
            # a separate mini html file 'search_results.html'.
            return_str = render_to_string(self.render_file, context)

            # Returns the mini html page as a JSON response to be displayed
            # in the search results on the index.html page.
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
        self.sql = '''SELECT player_name FROM searching_player
                        WHERE player_name LIKE %s'''
        # form properties
        self.placeholder = 'Enter player name'
        self.id = 'player-name-search'


class TeamSelection(View):

    def post(self, request):
        print('Team Selection POST')

        team_name = str(dict(request.POST)['general_input'][0])

        cursor = connection.cursor()
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
        player_names = merge_sort(list(map(lambda z: z[0], cursor.fetchall())))

        # creates a format which can be passed into the html
        context = Context({'player_names': player_names})

        # Adds the context to the correct place on the page, by passing into a
        # separate mini html file 'team_player_results.html'.
        return_str = render_to_string('team_player_results.html', context)
        return HttpResponse(
            json.dumps(return_str),
            content_type="application/json")


class Statistics(View):

    def __init__(self):
        self.cursor = connection.cursor()
        # properties below will be used to construct the sql query
        self.table = ""
        self.results = []

    def get_matches_played(self, name):
        self.cursor.execute("""SELECT 'Matches Played', COUNT(*) FROM
                            (SELECT DISTINCT match_id_id FROM scoring_ballbyball
                            WHERE onstrike=%s OR offstrike=%s)""",[name, name] )
        return self.cursor.fetchone()

    def get_total_runs_scored(self, name):
        self.cursor.execute("""SELECT 'Total Runs Scored', SUM(runs) FROM
                            (SELECT runs FROM scoring_ballbyball
                            WHERE onstrike=%s)""", [name])
        return self.cursor.fetchone()

    def get_high_score(self, name):
        self.cursor.execute("""SELECT 'High Score', MAX(sr) FROM
                            (SELECT SUM(runs) AS sr FROM scoring_ballbyball
                            WHERE onstrike=%s GROUP BY match_id_id)""", [name])
        return self.cursor.fetchone()

    def get_batting_average(self,name):
        # Total runs scored divided by total innings played
        self.cursor.execute("""SELECT 'Batting Average', AVG(sr) FROM
                            (SELECT SUM(runs) AS sr FROM scoring_ballbyball
                            WHERE onstrike=%s GROUP BY match_id_id)""", [name])
        return self.cursor.fetchone()

    def get_batting_strike_rate(self,name):
        # (Total runs scored / total balls faced ) * 100
        self.cursor.execute("""SELECT 'Batting Strike Rate', ar*100 FROM
                            (SELECT AVG(runs) as ar FROM scoring_ballbyball
                            WHERE onstrike=%s)""", [name])
        return self.cursor.fetchone()

    def get_bowling_runs(self, name):
        #
        self.cursor.execute("""SELECT 'Bowling Runs Conceded', SUM(runs) FROM
                            (SELECT runs FROM scoring_ballbyball
                            WHERE bowler=%s)""",[name])
        return self.cursor.fetchone()

    def get_wickets_taken(self, name):

        self.cursor.execute("""SELECT 'Wickets Taken', COUNT(*) FROM
                            (SELECT * FROM scoring_ballbyball
                            WHERE bowler=%s AND how_out<>'')""",[name])
        return self.cursor.fetchone()

    def get_best_bowling(self, name):
        self.cursor.execute("""SELECT 'Best Bowling', r||'/'||w FROM (
                            SELECT SUM(CASE how_out WHEN '' THEN 0 ELSE 1 END) AS w,
                            sum(runs) as r FROM scoring_ballbyball WHERE bowler=%s
                            GROUP BY match_id_id ORDER BY w DESC LIMIT 1)""", [name])
        return self.cursor.fetchone()

    def get_bowling_economy(self, name):
        # ( total runs scores / total balls bowled ) * 6
        # conversion to integer is needed
        self.cursor.execute("""SELECT 'Bowling Econ', (r/c)*6 FROM
                            (SELECT cast(SUM(runs) as float) as r,
                            cast(COUNT(*) as float) as c
                            FROM scoring_ballbyball
                            WHERE bowler=%s)""", [name])
        return self.cursor.fetchone()


class PlayerStatistics(Statistics, View):

    def __init__(self):
        super().__init__()
        self.table = "searching_player"
        self.column_name = "player_name"


    def post(self, request):
        form = GeneralTextForm(request.POST, class_name="", id="hidden-input")
        # Gives us the name of the player who has been selected in the client
        # side. This is the player about whom statistics are to be displayed.
        name = str(dict(request.POST)['general_input'][0])

        self.results = [self.get_matches_played(name), self.get_total_runs_scored(name),
                        self.get_high_score(name), self.get_batting_average(name),
                        self.get_batting_strike_rate(name), self.get_bowling_runs(name),
                        self.get_wickets_taken(name), self.get_best_bowling(name),
                        self.get_bowling_economy(name)]

        context = Context({'statistics': self.results})

        # Adds the context to the correct place on the page, by passing
        # into a separate mini html file 'team_player_results.html'.
        return_str = render_to_string('statistics.html', context)

        return HttpResponse(
            json.dumps(return_str),
            content_type="application/json")


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

    This is the view function to which the final POST request is made from the
    client side for the part of the app where teams and players are being selected.
    This will not be an AJAX POST but a normal HTTP POST. The job of this
    View class is to take all the details that have been input and put them in
    the correct location within the database so as to prepare the system to start
    scoring the actual game.
    """

    def __init__(self):
        # initialises the parent class ScoringInterface which is being inherited
        super().__init__()
        # opens up a database connection
        self.cursor = connection.cursor()

    # When a POST request is made to this view class, the POST request is
    # redirected to the post function below. This is only possible because the
    # class is inheriting the View class from DJANGO. The data being sent in the
    # POST request is being passed into the request parameter in the post
    # function below.
    def post(self, request):
        # Converts the posted data's format to a dictionary to make it easier to
        # manipulate and extract values from.
        match_details = dict(request.POST)
        print('MATCH DETAILS DICTIONARY SUBMISSION: {}'.format(match_details))
        #
        if match_details['ground_location'] == 'home':
            self.cursor.execute("""SELECT home_ground FROM searching_team
                                WHERE id=%s;""",[int(match_details['home_team'][0])])
        else:
            self.cursor.execute("""SELECT home_ground FROM searching_team
                                WHERE id=%s;""" %
                                (int(match_details['away_team'][0])))
        match_details['ground_location'] = self.cursor.fetchone()[0]

        # All the non integer data types need to be converted specific
        self.cursor.execute("""INSERT INTO searching_match
                            (date, ground_location, umpire_1, umpire_2, weather,
                            away_team_id, home_team_id, batting_first, overs)
                            VALUES (DATE('now'), %s, %s, %s, %s, %s, %s,
                            %s, %s)""", [match_details['ground_location'],
                                         match_details['umpire_1'][0],
                                         match_details['umpire_2'][0],
                                         match_details['weather'][0],
                                         int(match_details['away_team'][0]),
                                         int(match_details['home_team'][0]),
                                         match_details['batting_first'][0],
                                         int(match_details['overs'][0])])
        # Add all the players name to match team player with match id and
        # team id
        all_players = match_details["home_team_teamsheet"][0].split(',')
        all_players +=  match_details["away_team_teamsheet"][0].split(',')

        for player in all_players:
            self.cursor.execute("""SELECT id,current_team_name_id FROM
                                searching_player WHERE player_name =%s""",
                                [player])
            player_id, team_id = self.cursor.fetchone()
            self.cursor.execute("""SELECT id FROM searching_match
                                ORDER BY id DESC LIMIT 1""")
            match_id = self.cursor.fetchone()[0]
            self.cursor.execute("""INSERT INTO searching_MatchTeamPlayer
                                (player_id_id, team_id_id, match_id_id)
                                VALUES (%s, %s, %s)""",
                                [int(player_id), int(team_id), int(match_id)])
            # issue - the playerslists are being reutned as one long string

        # prepares ball-by-ball db for scoring by loading up the latest added
        # record in the matches db
        self.cursor.execute("""INSERT INTO scoring_ballbyball
                            (match_id_id, over, ball_in_over, total_runs,
                            total_wickets, runs, extras, innings) VALUES
                            ((SELECT id AS match_id_id FROM searching_match
                            ORDER BY match_id_id DESC LIMIT 1),0,0,0,0,0,0,1)""")
        return HttpResponseRedirect("/scoring/")

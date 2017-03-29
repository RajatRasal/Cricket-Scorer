from django.db import connection


class DatabaseStackImplementation:
    """
    I have implemented the main table in the database as a stack, such that the
    current ball displayed on the screen will be the last record in the table,
    when undoing a ball we are just removing the last record in the tables and
    when we bowl a new ball we are adding a record to the table
    """

    def __init__(self):
        # connector to the database
        self.items = connection.cursor()

    def peek(self):
        print('peek')
        # returns all the attribute/column names from the ball by ball table
        self.items.execute("""PRAGMA table_info(scoring_ballbyball)""")
        # gets all the data returned by the query from the buffers and converts
        # it to a more readable list format
        column_names = list(map(lambda x: x[1], list(self.items.fetchall())))
        # gets the last record from the ball by ball database, thus is it
        # getting the last ball that has been bowled in the game
        self.items.execute("""SELECT * FROM scoring_ballbyball ORDER BY id DESC LIMIT 1""")
        # gets all the data returned by the last query from the buffers and
        # converts it to a more readable list format
        last_ball = list(self.items.fetchone())
        # merges the columns names and the last ball lists to form a dictionary
        context = dict(zip(column_names, last_ball))
        return context

    def push(self, ball_event):
        self.items.execute("""INSERT INTO scoring_ballbyball
                           (onstrike, offstrike, bowler, over, ball_in_over,
                           total_runs, total_wickets, how_out, people_involved,
                           runs, extras, extras_type, match_id_id, innings) VALUES
                           (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                           """, [ball_event["onstrike"], ball_event["offstrike"],
                                 ball_event["bowler"], int(ball_event["over"]),
                                 int(ball_event["ball_in_over"]), int(ball_event["total_runs"]),
                                 int(ball_event["total_wickets"]), ball_event["how_out"],
                                 ball_event["people_involved"], int(ball_event["runs"]),
                                 int(ball_event["extras"]), ball_event["extras_type"],
                                 int(ball_event["match_id_id"]), int(ball_event["innings"])]
                           )

    def pop(self, ball_event):  # undo
        # Delete the current ball record in the database and then return
        # the new last record. We have essentially undone the events from the
        # previous ball since the data in the returned record will then be
        # updated in the client side.
        self.items.execute("""DELETE FROM scoring_ballbyball WHERE id=%s""",
                           [ball_event['id']])
        print(self.peek())
        return self.peek()


class Queries:

    def __init__(self):
        print('INITIALISNG QUERIES -----------------')
        self.cursor = connection.cursor()
        # Returns the value of the innings columns for the last record in the
        # scoring_ballbyball table.
        self.match_id, self.innings = self.cursor.execute("""SELECT match_id_id, innings
                                                          FROM scoring_ballbyball
                                                          ORDER BY id DESC LIMIT 1
                                                          """).fetchone()
        self.batting_first = self.cursor.execute("""SELECT batting_first FROM searching_match
                                         ORDER BY id DESC LIMIT 1""").fetchone()[0]
        # print('Match id: {} Innings: {} Batting First: {}'.format(
        #    self.match_id, self.innings, self.batting_first))
        # current_batting is a string with the name of the team currently
        # batting
        if (self.innings == 1 and self.batting_first == "home") or (
            self.innings == 2 and self.batting_first == "away"):
            # the current batting team will be the home team these conditions
            print('HOME')
            # self.current_batting = self.cursor.execute("""
            #                                SELECT home_team_id FROM searching_match
            #                                ORDER BY id DESC LIMIT
            #                                1""").fetchone()[0]
            # self.current_bowling = self.cursor.execute("""
            #                                SELECT away_team_id FROM searching_match
            #                                ORDER BY id DESC LIMIT
            #                                1""").fetchone()[0]
            self.current_batting, self.current_bowling = self.cursor.execute("""
                                            SELECT home_team_id, away_team_id FROM searching_match
                                            ORDER BY id DESC LIMIT 1""").fetchone()
            # self.current_bowling = self.cursor.execute("""SELECT away_team_id FROM searching_match
            #                                   ORDER BY id DESC LIMIT 1""").fetchone()[0]
        if (self.innings == 2 and self.batting_first == "home") or (
            self.innings == 1 and self.batting_first == "away"):
            # self.current_batting, self.current_bowling = self.cursor.execute("""
            #                                SELECT away_team_id, home_team_id FROM searching_match
            #                                ORDER BY id DESC LIMIT 1""").fetchone()[0]
            self.current_batting, self.current_bowling = self.cursor.execute("""
                                            SELECT away_team_id, home_team_id FROM searching_match
                                            ORDER BY id DESC LIMIT 1""").fetchone()
            # self.current_bowling = self.cursor.execute("""SELECT home_team_id FROM searching_match
            #                                   ORDER BY id DESC LIMIT 1""").fetchone()[0]

    def get_all_available_batters(self):
        # Gets all the player names from the searching_player table which have
        # been selected for the current match and returns their names
        self.cursor.execute("""select p.player_name from searching_player as p
                            inner join searching_matchteamplayer mtp
                            on mtp.player_id_id = p.id
                            where mtp.match_id_id=%s and mtp.team_id_id=%s""",
                            [self.match_id, self.current_batting])
        # add some code to make sure the batters are not in the mtp table either
        x = list(map(lambda x: x[0], list(self.cursor.fetchall())))
        print('ALL AVAILABLE BATTERS: ',x)
        return x

    def get_all_available_bowlers(self):
        # Gets all the player names from the searching_player table which have
        # been selected for the current match and returns their names
        self.cursor.execute("""select p.player_name from searching_player as p
                            inner join searching_matchteamplayer mtp
                            on mtp.player_id_id = p.id
                            where mtp.match_id_id=%s and mtp.team_id_id=%s""",
                            [self.match_id, self.current_bowling])
        # add some code to make sure the batters are not in the mtp table either
        x = map(lambda x: x[0], list(self.cursor.fetchall()))
        print('result:' ,x)
        return x

    def get_live_batter_stats(self, name):
        # print('GET LIVE BATTERS STATS')
        runs = self.cursor.execute("""SELECT SUM(runs) FROM scoring_ballbyball
                                   WHERE onstrike=%s AND match_id_id=%s""",
                                   [name, self.match_id]).fetchone()[0]
        balls = self.cursor.execute("""SELECT COUNT(*) FROM scoring_ballbyball
                                    WHERE onstrike=%s AND match_id_id=%s AND
                                    extras_type<>'wd' AND extras_type<>'nb'""",
                                    [name, self.match_id]).fetchone()[0]
        fours = self.cursor.execute("""SELECT COUNT(*) FROM scoring_ballbyball
                                    WHERE onstrike=%s AND match_id_id=%s AND
                                    runs=4""", [name, self.match_id]).fetchone()[0]
        sixes = self.cursor.execute("""SELECT COUNT(*) FROM scoring_ballbyball
                                    WHERE onstrike=%s AND match_id_id=%s AND
                                    runs=6""", [name, self.match_id]).fetchone()[0]
        # Exception handling for when a new batsman is in and they have not
        # scored any runs or faced any balls which will result in Nonetype
        # being returned from database query which cannot be divided to form the
        # strike_rate key in the x dictionary.
        try:
            # converted to strings so that they can be rendered in html without
            # any format conversion needed
            results = {'runs': int(runs), 'balls': int(balls),
                       'fours': int(fours), 'sixes': int(sixes),
                       'strike_rate': round(int(runs)/int(balls),2)}
        except Exception:
            results = {'runs':0, 'balls':0, 'fours':0, 'sixes':0, 'strike_rate':0}
        print('result: ', results)
        return results

    def get_live_bowler_stats(self, name):
        print('GET LIVE BOWLER STATS')
        runs = self.cursor.execute("""SELECT SUM(runs+extras) FROM scoring_ballbyball
                                   WHERE bowler=%s AND match_id_id=%s
                                   AND extras_type <> 'lb' AND extras_type <> 'b'
                                   AND extras_type <> 'penalties' """,
                                   [name, self.match_id]).fetchone()[0]
        print(runs)
        overs = self.cursor.execute("""SELECT COUNT(*) FROM (
                                    SELECT DISTINCT over FROM scoring_ballbyball
                                    WHERE bowler=%s AND match_id_id=%s )""",
                                    [name, self.match_id]).fetchone()[0]
        maidens = self.cursor.execute("""SELECT COUNT(*) FROM (
                                            SELECT over, SUM(runs)
                                            FROM scoring_ballbyball
                                            WHERE bowler=%s AND match_id_id=%s
                                            GROUP BY over
                                            HAVING SUM(runs)=0 )""",
                                      [name, self.match_id]).fetchone()[0]
        wickets = self.cursor.execute("""SELECT COUNT(*) FROM scoring_ballbyball
                                      WHERE how_out<>'' AND bowler=%s AND
                                      match_id_id=%s""",
                                      [name, self.match_id]).fetchone()[0]
        # Exception handling for when a new bowler is in and there are no runs
        # conceeded off their bowling so the data is returning null value which
        # cannot be converted to an integer in the results dictionary.
        try:
            print('TRY')
            results = {'runs': int(overs), 'balls': int(runs),
                       'fours': int(maidens), 'sixes': int(wickets),
                       'strike_rate': round(int(runs)/int(overs),2)}
        except Exception:
            print('EXCEPT')
            results = {'runs': int(overs), 'balls': 0, 'fours': int(maidens),
                       'sixes': int(wickets), 'strike_rate': 0}

        print('result: ', results)
        return results

    def get_last_ten_balls(self):
        # print('GET LAST 10 BALLS')
        last_10 = self.cursor.execute("""SELECT CASE WHEN how_out <> ''
                                                        THEN how_out
                                                     WHEN extras <> 0
                                                        THEN extras||extras_type
                                                     ELSE runs
                                                     END
                                      FROM scoring_ballbyball WHERE match_id_id =%s
                                      ORDER BY id DESC LIMIT 10""",
                                      [self.match_id]).fetchall()
        x = list(map(lambda x: x[0], list(last_10)))
        print('LAST 10 BALLS: ', x)
        return x

    def get_max_over_limit(self):
        pass

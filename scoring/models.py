"""
Contains the ball-by-ball table
"""

from django.db import models

from searching.models import Match


class BallByBall(models.Model):
    """
    """

    # Will store the match id of the latest game
    match_id = models.ForeignKey(Match, related_name='match_id',
                                 on_delete=models.PROTECT)
    onstrike = models.CharField(max_length=30, blank=True, null=True)
    offstrike = models.CharField(max_length=30, blank=True, null=True)
    bowler = models.CharField(max_length=30, blank=True, null=True)
    over = models.IntegerField(default=0, blank=True, null=True)
    ball_in_over = models.IntegerField(default=0, blank=True, null=True)
    total_runs = models.IntegerField(default=0, blank=True, null=True)
    total_wickets = models.IntegerField(default=0, blank=True, null=True)
    how_out = models.CharField(max_length=20, blank=True, null=True)
    people_involved = models.CharField(max_length=30, blank=True, null=True)
    runs = models.IntegerField(default=0, blank=True, null=True)
    extras = models.IntegerField(default=0, blank=True, null=True)
    extras_type = models.CharField(max_length=20, blank=True, null=True)
    innings = models.IntegerField(default=1)

    def __str__(self):
        return 'Match: {}, Ball: {}.{}'.format(self.match_id,
                                               self.over,
                                               self.ball_in_over)

if "__main__" == __name__:
    print(Match)

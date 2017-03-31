"""cricket_scoring URL Configuration
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')

Django is a Model View Controller framework as I have mentioned many times 
in my design and analysis. This purpose of this file in the client server
model is to direct requests to the correct view functions to be handled. 
The view function produces the display associated with a particular URL 
path name.

So when a request is made to http://localhost:PORT/startpage/, the below
pattern matching syntax, which uses regex to match URL patterns, is called 
and, in this case, causes the Index class to be run as a View function. 
The Index class wil therefore now be responsible for providing a 
HTTPResponse to the location from where the request for the /startpage/ was
made. 

IN SHORT --> THIS FILE MAPS URL PATH NAMES TO A CLASS, BY MATCHING THE PATH
NAMES USING REGEX. THE MAPPED CLASS WILL NOW BE RESPONSIBLE FOR SENDING BACK 
A HTML FOR DISPLAY OR ANY OTHER FORM OF HTTP RESPONSE TO THE CLIENT SIDE 
BROWSER. 
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

from searching.views import (Base, Index, TeamSearch, TeamSelection,
                             MatchDetails, PlayerSearch, PlayerStatistics)
from scoring.views import ScoringInterface

admin.autodiscover()

# These are all the URL paths names which are being matched by the 
# DJANGO web server. They are being matched using REGEX. 
# ^[path_name]/$ - after the start of the string there should be a path name
# with no spaces followed by a forward slash and then the string end.
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', Base.as_view()),
    url(r'^startpage/$', Index.as_view()),
    url(r'^team_search/$', TeamSearch.as_view()),
    url(r'^team_selection/$', TeamSelection.as_view()),
    url(r'^match_details/$', MatchDetails.as_view()),
    url(r'^player_search/$', PlayerSearch.as_view()),
    url(r'^player_stats/$', PlayerStatistics.as_view()),
    url(r'^scoring/$', MatchDetails.as_view()),
    url(r'^scoring_submit/$', ScoringInterface.as_view()),
    url(r'^get_scores/$', csrf_exempt(ScoringInterface.as_view())),
]


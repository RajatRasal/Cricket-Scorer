"""cricket_scoring URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

from searching.views import (Base, Index, TeamSearch,
                             TeamSelection, MatchDetails, PlayerSearch,
                             PlayerStatistics, AjaxTest)
from scoring.views import ScoringInterface

admin.autodiscover()

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
    url(r'^ajax_test/$', AjaxTest.as_view())
]

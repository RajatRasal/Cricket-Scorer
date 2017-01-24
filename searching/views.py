from django.shortcuts import render, render_to_response 
from django.views.generic import View

from searching.models import Team
from searching.forms import TeamnameSearchForm, MatchDetailsForm 

class Base(View):

	def get(self, request):
		return render(request, 'base.html')

class Index(View):

	def get(self, request):
		teamname_search_form = TeamnameSearchForm()
		match_details_form = MatchDetailsForm()
		
		return render(request, 'index.html', 
			{'teamname_form': teamname_search_form,
                        'match_details_form': match_details_form,})

class TeamSearch(View):

	def post(self, request):
                search_text = request.POST['search_text']
                #the bottom will need to be converted to SQL at a later date
                #'__contains' akin to sql LIKE command
                #options = Team.objects.filter(team_name__contains=search_text)
                team_names = Team.objects.filter(team_name__startswith=search_text)

                return render_to_response('ajax_team_search.html',
                        {'team_names': team_names})


if __name__ == "__main__":
	print('hi')
	print(TeamnameSearchForm)


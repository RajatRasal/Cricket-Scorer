import json
from re import *

from django.shortcuts import render, render_to_response, HttpResponse
from django.views.generic import View
from django.template import Context
from django.template.loader import render_to_string

from searching.models import Team
from searching.forms import TeamnameSearchForm, MatchDetailsForm, AjaxTestForm

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
			#check POC for comment details 
			print('SEARCH IS VALID')

			#takes the searched for text from the POST request
			query = form.cleaned_data['query']
			print('query: {}'.format(query))

			team_names = list(Team.objects.filter(team_name__icontains=query))

			#creates a format which can be passed into into the html
			context = Context({"query": query, "team_names": team_names})
			print('context: {}'.format(context))

			#Adds the context to the correct place in the 
			return_str = render_to_string('team_search.html', context)
			print('return str: {}'.format(return_str))

			return HttpResponse(json.dumps(return_str), content_type="application/json")
		else:
			return HttpResponse(json.dumps(""), content_type="application/json")
	
	
if __name__ == "__main__":
	print('hi')
	print(TeamnameSearchForm)


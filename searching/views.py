import json
		
from django.shortcuts import render, HttpResponse
from django.views.generic import View
from django.template import Context
from django.template.loader import render_to_string
#from django.views.decorators.csrf import csrf_protect
from django.db import connection
		
from searching.models import Team
from searching.forms import TeamnameSearchForm, MatchDetailsForm, GeneralTextForm, AjaxTestForm
		
class Base(View):
		
    def get(self, request):
	    return render(request, 'base.html')
		
class Index(View):
		
    def get(self, request):
        teamname_search_form = TeamnameSearchForm()
        match_details_form = MatchDetailsForm()
        hidden_text_input = GeneralTextForm(
                class_name="home-team",
                id="team-name-selection-input") 
        print('hidden text field: %s' % (str(hidden_text_input)))

        return render(request, 'index.html',
                {'team_name_form': teamname_search_form,
                'match_details_form': match_details_form,
                'hidden_text_input_form': hidden_text_input,}
                )

class TeamSearch(View):

    def post(self, request):
        print('Team Search POST')
        print('REQUEST', request)
        print('REQUEST', request.POST)
        form =  TeamnameSearchForm(request.POST)
        print(form)

        if form.is_valid():#Add my own validation here 
            print('INPUT IS VALID')

            #takes the searched for text from the POSt request and 'cleans' it 
            query = form.cleaned_data['query']
            print('cleaned input/query: {}'.format(query))

            #Querying the db with a command akin to like SQL statement (read the doc for details about __icontains)
            #converted to list in order to convert from db object to an iterable
            team_names = list(Team.objects.filter(team_name__icontains=query))

            #creates a format which can be passed into the html
            context = Context({'query': query, 'team_names': team_names})
            print('context: {}'.format(context))
        
            #Adds the context to the correct place on the page, by passing into a separate mini html file 'team_search_results.html'.
            return_str = render_to_string('team_search_results.html', context)
            print('returned string: {}'.format(return_str))

            #Returns the mini html page as a JSON response to be displayed 
            #in the search results on the index.html page.
            print("=================================================")
            return HttpResponse(json.dumps(return_str),content_type="application/json")

        else:
            return HttpResponse(json.dumps(""),content_type="application/json")


class TeamSelection(View):

    def post(self, request):
        print('Team Selection POST')
        #form = GeneralTextForm(request.POST)
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
        #fetchall returns query results in the format:
        #[('player 1',), ('player2',), ('player3',),...
        #This is not desirable when being displayed, so the map functions 
        #maps each tuple in the query results list to being just the player 
        #name string, so as to make the output look like this:
        #['player 1', 'player 2', 'player 3'...]
        #The output of the 'map' is returned as a 'map' object, so needs 
        #to be converted to a list.
        player_names = list(map(lambda z: z[0], cursor.fetchall())) 
        print(player_names)
        
        #creates a format which can be passed into the html
        context = Context({'player_names': player_names})
        print('context: {}'.format(context))
        
        #Adds the context to the correct place on the page, by passing into a separate mini html file 'team_player_results.html'.
        return_str = render_to_string('team_player_results.html', context)
        print('returned string: {}'.format(return_str))
        
        print("=================================================")

        return HttpResponse(json.dumps(return_str),content_type="application/json")
        '''
        if form.is_valid():#Add my own validation here 
            print('INPUT IS VALID')

            #takes the searched for text from the POSt request and 'cleans' it 
            query = form.cleaned_data['query']
            print('cleaned input/query: {}'.format(query))

            #Querying the db with a command akin to like SQL statement (read the doc for details about __icontains)
            #converted to list in order to convert from db object to an iterable
            team_names = list(Team.objects.filter(team_name__icontains=query))

            #creates a format which can be passed into the html
            context = Context({'query': query, 'team_names': team_names})
            print('context: {}'.format(context))
        
            #Adds the context to the correct place on the page, by passing into a separate mini html file 'team_search_results.html'.
            return_str = render_to_string('team_search_results.html', context)
            print('returned string: {}'.format(return_str))

            #Returns the mini html page as a JSON response to be displayed 
            #in the search results on the index.html page.
            return HttpResponse(json.dumps(return_str),content_type="application/json")
        else:
            return HttpResponse(json.dumps(""),content_type="application/json")
        '''
		
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
                return_str = render_to_string('team_search_results.html', context)
                print('return str: {}'.format(return_str))
                
                return HttpResponse(json.dumps(return_str), 
                                content_type="application/json")
            
        else:
            return HttpResponse(json.dumps(""), content_type="application/json")
		
		
if __name__ == "__main__":
    print('hi')
    print(TeamnameSearchForm)		

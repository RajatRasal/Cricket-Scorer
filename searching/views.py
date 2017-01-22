from django.shortcuts import render 
from django.views.generic import View

from searching.forms import TeamnameSearchForm, MatchDetailsForm, MatchDetailsTest

class Base(View):

	def get(self, request):
		return render(request, 'base.html')

class Index(View):

	def get(self, request):
		teamname_search_form = TeamnameSearchForm()
		match_details_form = MatchDetailsForm()
		match_details_form_test = MatchDetailsTest()
		
		return render(request, 'index.html', 
			{'teamname_form': teamname_search_form,
			'match_details_form': match_details_form,
			'match_details_test': match_details_form_test})


if __name__ == "__main__":
	print('hi')
	print(TeamnameSearchForm)
	print(MatchDetailsTest)


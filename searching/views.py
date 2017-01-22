from django.shortcuts import render 
from django.views.generic import View

from searching.forms import TeamnameSearchForm, MatchDetailsForm, MatchDetailsTest

class Base(View):

	def get(self, request):
		return render(request, 'base.html')

class Index(View):

	def get(self, request):
		TeamnameSearch = TeamnameSearchForm()
		MatchDetails = MatchDetailsForm()
		MatchTest = MatchDetailsTest()
		
		return render(request, 'index.html', 
			{'TeamnameSearchForm': TeamnameSearch,
			'MatchDetailsForm': MatchDetails,
			'MatchDetailsTest': MatchTest})


if __name__ == "__main__":
	print('hi')
	print(TeamnameSearchForm)
	print(MatchDetailsTest)


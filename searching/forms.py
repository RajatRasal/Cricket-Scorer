from django import forms

from .models import Match 

class TeamnameSearchForm(forms.Form):
    """
    """

    query = forms.CharField(
            widget=forms.TextInput(attrs={
                'placeholder':'Enter team name', 
                'class':'form-control', 
                'id':'team-name-search',
                'size': 160
                }), 
            label=False 
            )

class MatchDetailsForm(forms.ModelForm):
    """
    """
    
    class Meta:
	    model = Match
	    fields = ['ground_location', 'umpire_1', 'umpire_2', 'weather']

class AjaxTestForm(forms.Form):

	query = forms.CharField(
			label='Enter team name:',
			widget=forms.TextInput(
				attrs={
                                        'id': 'search-input',
					'size': 32,
					'class': 'form-control'
					})
				)

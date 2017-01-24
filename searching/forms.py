from django import forms

from .models import Match 

class TeamnameSearchForm(forms.Form):
    """
    """

    text = forms.CharField(
            widget=forms.TextInput(attrs={
                'placeholder':'Enter the home team name', 
                'class':'form-control', 
                'index':'team-name-search',
                }), 
            max_length=160,
            label=False 
            )

class MatchDetailsForm(forms.ModelForm):
    """
    """
    
    class Meta:
	    model = Match
	    fields = ['ground_location', 'umpire_1', 'umpire_2', 'weather']

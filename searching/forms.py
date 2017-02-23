from django import forms

from .models import Match 

class TeamnameSearchForm(forms.Form):
    """
    """
    def __init__(self, *args, **kwargs):
        self.placeholder = kwargs.pop('placeholder')
        self.id = kwargs.pop('id')
        super(TeamnameSearchForm, self).__init__(*args, **kwargs)
        self.fields['query'].widget = forms.TextInput(attrs={
            'placeholder':self.placeholder,
            'class':'form-control',
            'id':self.id,
            'size':160,
            'value':'',
            })

    query = forms.CharField(label=False)

#    query = forms.CharField(
#            widget=forms.TextInput(attrs={
#                'placeholder':'Enter team name', 
#                'class':'form-control', 
#                'id':'team-name-search',
#                'size': 160,
#                'value': '',
#                }), 
#            label=False 
#            )

class MatchDetailsForm(forms.ModelForm):
    """
    """
    
    class Meta:
	    model = Match
	    fields = ['ground_location', 'umpire_1', 
                    'umpire_2', 'weather', 'batting_first',
                    'overs', 'home_team','away_team']

class GeneralTextForm(forms.Form):
    """
    """

    def __init__(self, *args, **kwargs):
        self.class_name = kwargs.pop('class_name')
        self.id = kwargs.pop('id')
        super(GeneralTextForm, self).__init__(*args, **kwargs)
        self.fields['general_input'].widget = forms.TextInput(attrs={
            'placeholder':'General Input for anything',
            'id':self.id,
            'class':self.class_name,
            })

    general_input = forms.CharField(label=False)


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

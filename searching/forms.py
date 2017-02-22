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
                'size': 160,
                'value': '',
                }), 
            label=False 
            )

class MatchDetailsForm(forms.ModelForm):
    """
    """
    
    class Meta:
	    model = Match
	    fields = ['ground_location', 'umpire_1', 'umpire_2', 'weather']

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

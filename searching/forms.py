"""
File contains all the forms prodce by Django which make it easier for the client 
to make contact with the server side. These can be dynmically inserted into the HTML
and provide a faster direct access to the server side when a post request is made from 
those forms.
"""

from django import forms

from .models import Match


class TeamnameSearchForm(forms.Form):
    """
	Team names can be searched for in this form. This form will just be a 
	single input field.
    """
    def __init__(self,  *args,  **kwargs):
        self.placeholder = kwargs.pop('placeholder')
        self.id = kwargs.pop('id')
        super(TeamnameSearchForm,  self).__init__(*args,  **kwargs)
        # The keys in the 'attrs' dictionary are all html attributes. 
        self.fields['query'].widget = forms.TextInput(attrs={
            'placeholder': self.placeholder,
            'class': 'form-control',
            'id': self.id,
            'size': 160,
            'value': '',
            })
	# Charfield = text input box for input displayed in the client side
    query = forms.CharField(label=False)


class MatchDetailsForm(forms.ModelForm):
    """
    This form will be some input fields and some dropdown menus
    """

    class Meta:
        model = Match
        fields = ['ground_location', 'umpire_1', 'umpire_2', 'weather',
                  'batting_first', 'overs', 'home_team', 'away_team']


class GeneralTextForm(forms.Form):
    """
    This form will be used where ever you need a random text input field. So 
    as of yet this form has no specific purpose
    """

    def __init__(self,  *args,  **kwargs):
        self.class_name = kwargs.pop('class_name')
        self.id = kwargs.pop('id')
        super(GeneralTextForm,  self).__init__(*args,  **kwargs)
        # The keys in the 'attrs' dictionary are all html attributes.
        self.fields['general_input'].widget = forms.TextInput(attrs={
            'placeholder': 'General Input for anything',
            'id': self.id,
            'class': self.class_name,
            })

	# Charfield = text input box for input displayed in the client side
    general_input = forms.CharField(label=False)

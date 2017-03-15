"""
File will contain the code to produce the data inputs for the scoring
section of the web app. VERY IMPORTANT
"""

from django import forms


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


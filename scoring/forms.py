"""
File will contain the code to produce the data inputs for the scoring
section of the web app. VERY IMPORTANT

File contains all the forms prodce by Django which make it easier for the client 
to make contact with the server side. These can be dynmically inserted into the HTML
and provide a faster direct access to the server side when a post request is made from 
those forms.
"""

from django import forms


class TeamnameSearchForm(forms.Form):
    """
	Team names can be searched for in this form. This form will just be a 
	single input field.
    """
    def __init__(self, *args, **kwargs):
        self.placeholder = kwargs.pop('placeholder')
        self.id = kwargs.pop('id')
        super(TeamnameSearchForm, self).__init__(*args, **kwargs)
        # The keys in the 'attrs' dictionary are all html attributes.
        self.fields['query'].widget = forms.TextInput(attrs={
            'placeholder':self.placeholder,
            'class':'form-control',
            'id':self.id,
            'size':160,
            'value':'',
            })

	# Charfield = text input box for input displayed in the client side
    query = forms.CharField(label=False)
    
    
    
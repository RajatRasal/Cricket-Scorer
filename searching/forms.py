from django import forms

class TeamnameSearchForm(forms.Form):
    """
    """

    text = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder':'Enter the home team name', 'class':'form-control'}), 
            max_length=160,
            label=False 
            )

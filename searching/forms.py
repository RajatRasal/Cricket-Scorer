from django import forms


from .models import Match 

class TeamnameSearchForm(forms.Form):
    """
    """

    text = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder':'Enter the home team name', 'class':'form-control'}), 
            max_length=160,
            label=False 
            )

class MatchDetailsForm(forms.Form):
    """
    """
    
    #WEATHERCHOICES = ['sunny', 'sunny spells', 'cloudy', 'overcast', 'showers', 'heavy rain', 'rain and sun', 'other']
    ground = forms.CharField(label="Ground Location")
#    weather = forms.CharField(label="Weather")
#    umpire1 = forms.CharField(label="Home Umpire") 
#    umpire2 = forms.CharField(label="Away Umpire") 
#    matchformat = forms.IntegerField(label="Match Format", min_value="5", max_value="60") 

class MatchDetailsTest(forms.ModelForm):
    """
    """

    class Meta:
	    model = Match
	    fields = ('ground_location', 'umpire_1', 'umpire_2', 'weather')
    #WEATHERCHOICES = ['sunny', 'sunny spells', 'cloudy', 'overcast', 'showers', 'heavy rain', 'rain and sun', 'other']
    #weather = forms.ChoiceField(choices=WEATHERCHOICES)
    #weather = forms.CharField(label="Weather")
    #CHOICES = (('1', 'First',), ('2', 'Second',))
    #choice_field = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

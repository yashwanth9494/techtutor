from django import forms
from .models import *

class courseconceptform(forms.ModelForm):
    class Meta:
        model = courseconcept
        fields = '__all__'


class coursemodelform(forms.ModelForm):
    courselist = forms.ModelMultipleChoiceField(
        queryset=courseconcept.objects.all(),
        widget = forms.CheckboxSelectMultiple,  
    )
    class Meta:
        model = coursemodel
        fields = '__all__'



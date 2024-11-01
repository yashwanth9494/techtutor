from django import forms
from .models import *
from frontend1.models import CustomUser

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


class admin_user_form(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

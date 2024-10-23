from django import forms
from .models import CustomUser
from django.contrib.auth.hashers import make_password
import os

class regform(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['fullname','email','phone_no','password']

    def save(self):
        pass_hash = super().save(commit=False)
        custom_salt = os.urandom(16).hex()
        pass_hash.password = make_password(self.cleaned_data['password'], hasher='argon2', salt=custom_salt)
        pass_hash.save()
        return pass_hash
    
class loginform(forms.Form): 
    email = forms.EmailField()
    password = forms.CharField(max_length=30)

class Updateform(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['fullname','email','phone_no']

class changepasswordform(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['password']

    def save(self):
        pass_hash = super().save(commit=False)
        custom_salt = os.urandom(16).hex()
        pass_hash.password = make_password(self.cleaned_data['password'], hasher='argon2', salt=custom_salt)
        pass_hash.save()
        return pass_hash

    
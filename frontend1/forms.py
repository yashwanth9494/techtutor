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
    email = forms.EmailField(required=False)  # Optional email field

    class Meta:
        model = CustomUser
        fields = ['password']
        widgets = {
            'password': forms.PasswordInput(),  # Hides password input
        }

    def __init__(self, *args, **kwargs):
        user_instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)

        # Show email field only if no user instance is provided
        if user_instance is None:
            self.fields['email'].required = True
            self.fields['email'].widget = forms.EmailInput(attrs={'placeholder': 'Enter your email'})
        else:
            self.fields.pop('email', None)  # Remove email field if instance is provided

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Check if the email corresponds to an existing user
        if email and not CustomUser.objects.filter(email=email).exists():
            raise ValidationError("User with this Email does not exist.")
        
        return email
    

    def save(self):
        pass_hash = super().save(commit=False)
        custom_salt = os.urandom(16).hex()
        pass_hash.password = make_password(self.cleaned_data['password'], hasher='argon2', salt=custom_salt)
        pass_hash.save()
        return pass_hash

    
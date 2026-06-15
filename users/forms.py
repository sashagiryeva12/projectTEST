from django import forms
from .models import *
class SignUpForm(forms.Form):
    username = forms.CharField(
        max_length=100, 
        required=True,
        label='Имя пользователя',
        widget=forms.TextInput(
            attrs={
                'class': 'username'
            }
        )  
    )
    email = forms.EmailField(required=True, label='Почта')
    phone_number = forms.CharField(max_length=20, required=True)
    role = forms.ChoiceField(choices=StUser.USER_ROLES)
    password = forms.CharField(max_length=150, required=True)
    
class SignInForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label='Имя пользователя')
    password = forms.CharField(max_length=150, required=True, label='Пароль')
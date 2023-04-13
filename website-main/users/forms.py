from users.models import Profile
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields

class UserRegisterForm(UserCreationForm):
    email= forms.EmailField()

    class Meta:
        model = User
        fields=['username','email','password1','password2']

    

class UserUpdateForm(forms.ModelForm):
    email= forms.EmailField()

    class Meta:
        model = User
        fields=['username','email']


class UserDetailForm(forms.ModelForm):

    class Meta:
        model=Profile
        fields=['roll_no','college','type']



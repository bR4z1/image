from django import forms
from django.contrib.auth.models import User

from .models import AlbumPhoto


class AlbumForm(forms.ModelForm):

    class Meta:
        model = AlbumPhoto
        fields = ['photo_title', 'genre', 'photo_logo']

class AlbumForm1(forms.ModelForm): # не правильно - но работает! hidden how?

    class Meta:
        model = AlbumPhoto
        fields = ['photo_title', 'genre', 'photo_logo','height_field','width_field']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class ImageChangeForm(forms.Form):
    CHOICES = (
        ('L', 'black-white'),
        ('BLUR', 'blur'),
        ('1', 'white-pixel'),


        )
    Choise = forms.ChoiceField(choices=CHOICES, required=True)
    
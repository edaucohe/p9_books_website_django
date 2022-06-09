from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from . import models


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username',)


class SignInForm(forms.Form):
    username = forms.CharField(max_length=100, label="Nom d'utilisateur")
    password = forms.CharField(max_length=50, widget=forms.PasswordInput, label="Mot de passe")


class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ('image',)


class TicketForm(forms.ModelForm):
    # edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ['title', 'description']


# class DeleteTicketForm(forms.Form):
#     delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

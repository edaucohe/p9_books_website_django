from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username',)


# class SignUpForm(forms.Form):
#     username = forms.CharField(max_length=100, label="Nom d'utilisateur")
#     password = forms.CharField(max_length=50, widget=forms.PasswordInput, label="Mot de passe")
#     password_confirmation = forms.CharField(max_length=50, widget=forms.PasswordInput, label="Confirmer mot de passe")


class SignInForm(forms.Form):
    username = forms.CharField(max_length=100, label="Nom d'utilisateur")
    password = forms.CharField(max_length=50, widget=forms.PasswordInput, label="Mot de passe")


class TicketForm(forms.Form):
    title = forms.CharField(max_length=128, label="Titre")
    description = forms.CharField(max_length=2048, widget=forms.Textarea)

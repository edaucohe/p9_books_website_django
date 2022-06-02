from django import forms


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=100, label="Nom d'utilisateur")
    password = forms.CharField(max_length=50, widget=forms.PasswordInput, label="Mot de passe")
    password_confirmation = forms.CharField(max_length=50, widget=forms.PasswordInput, label="Confirmer mot de passe")


class SignInForm(forms.Form):
    username = forms.CharField(max_length=100, label="Nom d'utilisateur")
    password = forms.CharField(max_length=50, widget=forms.PasswordInput, label="Mot de passe")

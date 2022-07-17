from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from . import models


# Signing forms
class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username',)
        labels = {'username': "Nom d'utilisateur "}


class SignInForm(forms.Form):
    username = forms.CharField(max_length=100, label="Nom d'utilisateur ")
    password = forms.CharField(max_length=50, widget=forms.PasswordInput, label="Mot de passe ")


# Ticket Forms
class PhotoForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = models.Photo
        fields = ('image',)


class DeletePhotoForm(forms.Form):
    delete_photo = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ['title', 'description']
        labels = {'title': "Titre ", 'description': "Description "}


class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


# Review forms
class ReviewForm(forms.ModelForm):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Review
        fields = ['headline', 'body', 'rating']
        labels = {'headline': "Titre ", 'body': "Commentaire ", 'rating': "Note "}


class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


# Follow forms
class FollowUsersForm(forms.ModelForm):
    class Meta:
        model = models.UserFollows
        fields = ['followed_user']
        labels = {'followed_user': "Utilisateurs actuels "}


class DeleteSubscriptionForm(forms.Form):
    delete_subscription = forms.BooleanField(widget=forms.HiddenInput, initial=True)

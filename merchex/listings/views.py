from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
# from django.views.decorators.csrf import csrf_protect
# from listings.forms import SignUpForm, SignInForm
# from . import forms
from listings import forms


def log_out(request):
    logout(request)
    return redirect('sign-in')


# @csrf_protect
def sign_up(request):
    # ceci doit être une requête POST, donc le formulaire est rempli
    # message = ""
    if request.method == 'POST':
        # créer une instance de notre formulaire "rempli" avec les données du POST
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return redirect('dashboard')

    else:
        form = forms.SignUpForm()

    # passe ce formulaire au gabarit
    return render(request, 'listings/sign_up.html', context={'form': form})


# @csrf_protect
def sign_in(request):
    if request.method == 'POST':
        # créer une instance de notre formulaire "rempli" avec les données du POST
        form = forms.SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('dashboard')

    else:
        form = forms.SignInForm()

    return render(request, 'listings/sign_in.html', {'form': form})


# def sign(request):
#     if request.method == 'POST':
#         sign_up_form = forms.SignUpForm(request.POST)
#         sign_in_form = forms.SignInForm(request.POST)
#
#         # Sign up form
#         if 'sign_up_btn' in request.POST:
#             sign_up_form = forms.SignUpForm(request.POST)
#             if sign_up_form.is_valid():
#                 sign_up_user = authenticate(
#                     username=sign_up_form.cleaned_data['username'],
#                     password=sign_up_form.cleaned_data['password'],
#                     password_confirmation=sign_up_form.cleaned_data['password_confirmation'],
#                 )
#                 if sign_up_user is not None:
#                     login(request, sign_up_user)
#                     return redirect('dashboard')
#
#         # Sign in form
#         elif 'sign_in_btn' in request.POST:
#             sign_in_form = forms.SignInForm(request.POST)
#             if sign_in_form.is_valid():
#                 sign_in_user = authenticate(
#                     username=sign_in_form.cleaned_data['username'],
#                     password=sign_in_form.cleaned_data['password'],
#                 )
#                 if sign_in_user is not None:
#                     login(request, sign_in_user)
#                     return redirect('dashboard')
#
#     else:
#         sign_up_form = forms.SignUpForm()
#         sign_in_form = forms.SignInForm()
#
#     return render(request, 'listings/sign.html', {'sign_up_form': sign_up_form, 'sign_in_form': sign_in_form})


@login_required
def dashboard(request):
    return render(request, 'listings/dashboard.html')


# @login_required
# def photo_upload(request):
#     form = forms.PhotoForm()
#     if request.method == 'POST':
#         form = forms.PhotoForm(request.POST, request.FILES)
#         if form.is_valid():
#             photo = form.save(commit=False)
#             # set the uploader to the user before saving the model
#             photo.uploader = request.user
#             # now we can save
#             photo.save()
#             return redirect('home')
#     return render(request, 'blog/photo_upload.html', context={'form': form})


@login_required
def create_tickets(request):
    ticket_form = forms.TicketForm()
    photo_form = forms.PhotoForm()
    if request.method == 'POST':
        # handle the POST request here
        ticket_form = forms.TicketForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        if all([ticket_form.is_valid(), photo_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()

            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.photo = photo
            ticket.save()

            return redirect('dashboard')

    forms_as_context = {
        'ticket_form': ticket_form,
        'photo_form': photo_form,
    }
    return render(request, 'listings/tickets.html', context=forms_as_context)


# def tickets(request):
#     if request.method == 'POST':
#         tickets_form = TicketsForm()
#     return render(request, 'listings/tickets.html')

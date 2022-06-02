from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

# Create your views here.
# from django.views.decorators.csrf import csrf_protect
from listings.forms import SignUpForm


# def log_out(request):
#     logout(request)
#     return redirect('sign_up')


# @csrf_protect
def sign_up(request):
    # ceci doit être une requête POST, donc le formulaire est rempli
    # message = ""
    if request.method == 'POST':
        # créer une instance de notre formulaire "rempli" avec les données du POST
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                password_confirmation=form.cleaned_data['password_confirmation'],
            )
            if user is not None:
                login(request, user)
                # message = f'Bonjour, {user.username}! Vous êtes connecté.'
                return redirect('dashboard')
            # else:
                # message = 'Identifiants invalides.'

            # ajoutez cette instruction de retour
            # return redirect('dashboard')

    # ceci doit être une requête GET, donc créer un formulaire vide
    else:
        form = SignUpForm()

    # passe ce formulaire au gabarit
    return render(request, 'listings/sign_up.html', {'form': form})


def dashboard(request):
    return render(request, 'listings/dashboard.html')

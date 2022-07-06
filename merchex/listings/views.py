from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

# Create your views here.
# from django.views.decorators.csrf import csrf_protect
# from listings.forms import SignUpForm, SignInForm
# from . import forms
from listings import forms
from . import models


def log_out(request):
    logout(request)
    return redirect('sign')


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
                return redirect('flux')

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
                return redirect('flux')

    else:
        form = forms.SignInForm()

    return render(request, 'listings/sign_in.html', {'form': form})


def sign(request):
    if request.method == 'POST':
        sign_up_form = forms.SignUpForm(request.POST)
        sign_in_form = forms.SignInForm(request.POST)

        # Sign up form
        if 'sign_up_btn' in request.POST:
            sign_up_form = forms.SignUpForm(request.POST)
            if sign_up_form.is_valid():
                user = sign_up_form.save()
                if user is not None:
                    login(request, user)
                    return redirect('flux')

        # Sign in form
        elif 'sign_in_btn' in request.POST:
            sign_in_form = forms.SignInForm(request.POST)
            if sign_in_form.is_valid():
                sign_in_user = authenticate(
                    username=sign_in_form.cleaned_data['username'],
                    password=sign_in_form.cleaned_data['password'],
                )
                if sign_in_user is not None:
                    login(request, sign_in_user)
                    return redirect('flux')

    else:
        sign_up_form = forms.SignUpForm()
        sign_in_form = forms.SignInForm()

    return render(request, 'listings/sign.html', {'sign_up_form': sign_up_form, 'sign_in_form': sign_in_form})


@login_required
def flux(request):
    user = request.user
    # SELECT tickets.*, photo.*
    # FROM tickets
    # LEFT OUTER JOIN photos ON tickets.photo_id = photos.id
    # WHERE user_id = 5
    #       tickets.id, tickets.user_id , ..., photos.id, photos.url
    # 1     1         , 5               ,...., null     , null
    # 2     3         , 5               ,...., 1        , 'https://......'

    # Ticket(id=1, ..., photo=null)
    # Ticket(id=3, ..., photo=Photo(id=1, url='https://....'))

    # SELECT * FROM tickets WHERE user_id = 5  -> [Ticket(id=1,...), Ticket(id=3, ....)]
    # ticket.photo for ticket in tickets
    #   SELECT * FROM photos WHERE id=<photo_id>

    tickets = list(models.Ticket.objects.filter(Q(user=user)))
    reviews = list(models.Review.objects.filter(Q(user=user)))

    followed_users = models.UserFollows.objects.filter(user=user)
    followed_user_ids = [u.followed_user.id for u in followed_users]
    follows_tickets = list(models.Ticket.objects.filter(user__id__in=followed_user_ids))
    follows_reviews = list(models.Review.objects.filter(user__id__in=followed_user_ids))

    all_reviews = reviews + follows_reviews
    all_tickets = tickets + follows_tickets
    ticket_ids_with_review = {review.ticket.id for review in all_reviews}

    # Remove redundant posts (like tickets with an existing review)
    all_posts = all_reviews + all_tickets
    all_posts = sorted(all_posts, key=lambda x: x.time_created, reverse=True)
    # for followed_user in followed_users:
    #     follows_tickets.append())
    #     follows_photos.append(models.Photo.objects.filter(Q(uploader=followed_user.user)))

    models_as_context = {
        'username': user,
        'all_posts': all_posts,
        'ticket_ids_with_review': ticket_ids_with_review
        # 'tickets': tickets,
        # 'reviews': reviews,
        # 'follows_tickets': follows_tickets,
        # 'follows_reviews': follows_reviews,
    }
    return render(request, 'listings/flux.html', context=models_as_context)


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

            return redirect('flux')

    forms_as_context = {
        'ticket_form': ticket_form,
        'photo_form': photo_form,
    }
    return render(request, 'listings/tickets.html', context=forms_as_context)


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    delete_form = forms.DeleteTicketForm()

    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_form = forms.TicketForm(request.POST, instance=ticket)

            if edit_form.is_valid():
                edit_form.save()
                return redirect('flux')

        if 'delete_ticket' in request.POST:
            delete_form = forms.DeleteTicketForm(request.POST)

            if delete_form.is_valid():
                ticket.delete()
                return redirect('flux')

    forms_as_context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'listings/edit_ticket.html', context=forms_as_context)


@login_required
def posts(request):
    username = request.user.username
    tickets = models.Ticket.objects.filter(Q(user__username__iexact=username))
    photos = models.Photo.objects.filter(Q(uploader__username__iexact=username))

    models_as_context = {
        'username': username,
        'tickets': tickets,
        'photos': photos
    }
    return render(request, 'listings/posts.html', context=models_as_context)


@login_required
def create_review(request, ticket_id):
    # username = request.user.username
    review_form = forms.ReviewForm()
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    # ticket = models.Ticket.objects.filter(Q(user__username__iexact=username))

    if request.method == 'POST':
        # handle the POST request here
        review_form = forms.ReviewForm(request.POST)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            return redirect('flux')

    return render(request, 'listings/create_review.html', context={'review_form': review_form})


@login_required
def show_reviews(request):
    username = request.user.username
    reviews = models.Review.objects.filter(Q(user__username__iexact=username))

    models_as_context = {
        'username': username,
        'reviews': reviews,
    }
    return render(request, 'listings/reviews.html', context=models_as_context)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    review_form = forms.ReviewForm(instance=review)
    delete_form = forms.DeleteReviewForm()

    if request.method == 'POST':
        if 'edit_review' in request.POST:
            review_form = forms.ReviewForm(request.POST, instance=review)

            if review_form.is_valid():
                review_form.save()
                return redirect('flux')

        if 'delete_review' in request.POST:
            delete_form = forms.DeleteReviewForm(request.POST)

            if delete_form.is_valid():
                review.delete()
                return redirect('flux')

    forms_as_context = {
        'edit_form': review_form,
        'delete_form': delete_form,
    }
    return render(request, 'listings/edit_review.html', context=forms_as_context)


@login_required
def subscriptions(request):
    my_follows = models.UserFollows.objects.filter(user=request.user)
    my_followers = models.UserFollows.objects.filter(followed_user=request.user)

    # id_current_user = request.user.id
    # username_current_user = request.user.username
    # current_user = request.user
    #
    # users_follows = models.UserFollows.objects.all()
    # user_follow = [user_follow for user_follow in users_follows]
    # user_follow_id = [user_follow.id for user_follow in users_follows]
    #
    # user_follow_user = [user_follow.user for user_follow in users_follows]
    # user_follow_user_id = [user_follow.user.id for user_follow in users_follows]
    # user_follow_user_username = [user_follow.user.username for user_follow in users_follows]
    #
    # user_follow_followed_user = [user_follow.followed_user for user_follow in users_follows]
    # user_follow_followed_user_id = [user_follow.followed_user.id for user_follow in users_follows]
    # user_follow_followed_user_username = [user_follow.followed_user.username for user_follow in users_follows]

    message = ""
    followed_form = forms.FollowUsersForm()
    if 'followed_user' in request.POST:
        # followed_user_post_username = request.POST.get('followed_user', False)
        # user_to_follow_from_post = models.User.objects.get(username=followed_user_post_username)
        followed_user_post_id = int(request.POST.get('followed_user', False))
        user_to_follow_from_post = models.User.objects.get(id=followed_user_post_id)
        # followed_form = forms.FollowUsersForm(request.POST, {'followed_user': user_to_follow_from_post})
        followed_form = forms.FollowUsersForm(request.POST)

        # if all([followed_form.is_valid(), delete_form.is_valid()]):
        if followed_form.is_valid():
            follow_form = followed_form.save(commit=False)
            follow_form.user = request.user
            follow_form.followed_user = user_to_follow_from_post
            follow_form.save()
            message = "Abonnement réussi !"

    # if 'delete_subscription' in request.POST:
    #     # for my_follower in my_followers:
    #     if delete_form.is_valid():
    #         delete_form.delete()
    #         message = "Désabonnement réussi !"

    models_as_context = {
        'request_user': request.user,
        'followed_user_objects': my_follows,
        'follower_user_objects': my_followers,
        'followed_form': followed_form,
        # 'delete_form': delete_form,
        'message': message,
    }

    return render(request, 'listings/subscriptions.html', context=models_as_context)


# @login_required
# def delete_subscription(request, subscription_id):
#     follow = get_object_or_404(models.UserFollows, id=subscription_id)
#     delete_form = forms.DeleteReviewForm()
#
#     if 'delete_subscription' in request.POST:
#         delete_form = forms.DeleteSubscriptionForm(request.POST)
#
#         if delete_form.is_valid():
#             follow.delete()
#
#     forms_as_context = {
#         'delete_form': delete_form,
#     }
#     return render(request, 'listings/delete_subscription.html', context=forms_as_context)

"""merchex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from listings import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.root, name='index'),
    # path('', views.forms, name='forms'),
    # path('sign', views.sign, name='sign'),
    # path('sign/', views.sign, name='sign'),
    path('sign_up/', views.sign_up, name='sign-up'),
    path('sign_in/', views.sign_in, name='sign-in'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('posts/', views.posts, name='posts'),
    # path('suscriptions/', views.suscriptions, name='suscriptions'),
    path('tickets/', views.create_tickets, name='tickets'),
    path('log_out/', views.log_out, name='log-out'),
    path('ticket/<int:ticket_id>/edit/', views.edit_ticket, name='edit_ticket'),
    path('review/<int:ticket_id>/create/', views.create_review, name='create_review'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

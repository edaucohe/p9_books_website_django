from django.contrib import admin
from listings.models import User, Ticket, Review, UserFollows, Photo


# Register your models here.
admin.site.register(User)
admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(UserFollows)
admin.site.register(Photo)

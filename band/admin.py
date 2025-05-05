from django.contrib import admin
from .models import PastEvent, Comments, Likes, Bookings, UpcomingEvent

# Register your models here.
admin.site.register(PastEvent)
admin.site.register(Comments)
admin.site.register(Likes)
admin.site.register(Bookings)
admin.site.register(UpcomingEvent)

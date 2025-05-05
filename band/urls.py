from django.urls import path, include
from . import views

app_name = "band"
urlpatterns = [
    path("", views.home, name="home"),
    path("events", views.events, name="events"),
    path("like_event/<int:event_id>", views.like_event, name="like_event"),
    path("comment/<int:event_id>", views.comment, name="comment"),
    path("details/<int:pk>", views.ModelDetailView.as_view(), name="details"),
    path("bookings", views.booking, name="booking"),
    path("mybookings", views.my_bookings, name="my_bookings"),
    path("", include("auth_app.urls")),
]

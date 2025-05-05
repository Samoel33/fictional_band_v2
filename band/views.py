from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from .forms import CommentsForm, BookingsForm
from .models import PastEvent, Comments, Likes, Bookings, UpcomingEvent
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import DetailView
from django.utils import timezone


# Create your views here.
def home(req):
    return render(req, "home.html")


def events(req):
    """
    View to display past and upcoming events.
    This view retrieves all past events and upcoming events,
    and deletes any past events from the upcoming events list.
    It also creates dictionaries to hold comments and likes per event.
    The view handles the form for comments and likes.

    Args:
        req (_type_): the Function takes a request object as an argument.


    Returns:
       returns the rendered template with past and upcoming events,
         comments, likes, and the comment form.
    """
    past_events = PastEvent.objects.all().order_by("-date")[:25]
    up_coming_events = UpcomingEvent.objects.all().order_by("-date")[:25]
    for event in up_coming_events:
        if event.date < timezone.now().date():
            PastEvent.objects.create(
                name=event.name,
                description=event.description,
                date=event.date,
                location=event.location,
            )
            event.delete()

    # Create dictionaries to hold comments and likes per event
    all_comments = {
        event.id: Comments.objects.filter(event=event) for event in past_events
    }
    all_likes = {event.id: Likes.objects.filter(event=event) for event in past_events}
    form = CommentsForm()
    return render(
        req,
        "events.html",
        {
            "past_events": past_events,
            "up_coming_events": up_coming_events,
            "all_comments": all_comments,
            "all_likes": all_likes,
            "form": form,
        },
    )


class ModelDetailView(DetailView):
    """
    View to display details of a specific event.
    This view retrieves the event based on the provided primary key (pk)
    and renders the details template with the event information.

    Args:
        DetailView (_type_): Django's generic view for displaying
        a single object.

    """

    model = PastEvent
    template_name = "details.html"
    context_object_name = "event"


@login_required
def like_event(req, event_id):
    """
    View to handle liking and unliking events.
    This view retrieves the event based on the provided event_id,
    and toggles the like status for the user.
    If the user has already liked the event, it removes the like.
    If the user has not liked the event, it adds a like.
    This view is protected by the login_required decorator,

    Args:
        req (_type_): the Function takes a request object as an argument.
        It is used to access the user making the request.
        event_id (_type_): The ID of the event to be liked or unliked.
        It is used to retrieve the specific event from the database.

    Returns:
        returns an HTTP response redirecting to the events page.
        If the user is not logged in,
        they will be redirected to the login page.
    """
    event = get_object_or_404(PastEvent, pk=event_id)

    like = Likes.objects.filter(user=req.user, event=event).first()

    if like:
        like.delete()
    else:
        Likes.objects.create(user=req.user, event=event)

    return HttpResponseRedirect(reverse("band:events"))


@login_required
def comment(req, event_id):
    """
    View to handle comments on events.
    This view retrieves the event based on the provided event_id,
    and processes the comment form submission.
    If the request method is POST, it validates the form and
    saves the comment.
    If the form is valid, it redirects to the events page.

    Args:
        req (_type_): the Function takes a request object as an argument.
        event_id (_type_): The ID of the event for which the comment -
        is being made.

    Returns:
        returns the rendered template with the comment form.
        If the form is valid, it redirects to the events page.
    """
    event = PastEvent.objects.get(pk=event_id)
    if req.method == "POST":
        form = CommentsForm(req.POST, user=req.user, event=event)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("band:events"))
    else:
        form = CommentsForm()
    return render(req, "events.html", {"form": form})


@login_required()
def my_bookings(req):
    """
    View to display the user's bookings.
    This view retrieves all bookings made by the user
    and deletes any past bookings.
    Args:
    req (_type_): the Function takes a request object as an argument.
    It is used to access the user making the request and to render the
    template with the user's bookings.

    Returns:
        returns the rendered template with the user's bookings.
    """
    bookings = Bookings.objects.filter(user=req.user).order_by("-booking_date")
    for booking in bookings:
        print(booking.band_response)
        if booking.booking_date < timezone.now().date():
            booking.delete()
    return render(req, "my_bookings.html", {"bookings": bookings})


@login_required()
def booking(req):
    """
    View to handle booking requests.
    Iterates through all upcoming events and deletes any that are past.
    save past events to the PastEvent model from upcoming events.
    Checks if the booking date is valid and not conflicting
    with any upcoming events.
    If the form is valid, it saves the booking and
    redirects to the events page.
    If the request method is not POST, it initializes a new form.
    Finally, it renders the booking template with the form.
    Args:
        req (_type_): The request object containing the booking data.
    Returns:
        HttpResponseRedirect: Redirects to the events page
        after processing the booking.
        renders the booking template with the form if not POST.
    """
    for event in UpcomingEvent.objects.all():
        PastEvent.objects.create(
            name=event.name,
            description=event.description,
            date=event.date,
            location=event.location,
        )
        event.delete()

    if req.method == "POST":
        form = BookingsForm(req.POST, user=req.user)
        print(req.user)
        booking_date = form.data.get("booking_date")

        if booking_date:
            for event in UpcomingEvent.objects.all():
                if event.date == booking_date:
                    form.add_error(
                        "booking_date",
                        "There is an upcoming event on this date. Please choose another date.",
                    )
                    break

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("band:events"))
    else:
        form = BookingsForm(user=req.user)
    return render(req, "bookings.html", {"form": form})

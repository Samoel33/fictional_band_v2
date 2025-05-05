from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class BaseEvent(models.Model):
    """
    Abstract base class for events.

    Fields:
        - name: Name/title of the event.
        - description: Optional description or summary of the event.
        - date: Date on which the event takes place.
        - location: Venue or place where the event is held.
        - image: Optional image representing the event.

    Notes:
        - This model is marked as abstract, meaning it will not create
        its own database table.
        - Intended to be inherited by concrete models like PastEvent
        and UpcomingEvent.
    """

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    date = models.DateField()
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to="event_images/", null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        """
        Returns a string representation of the event.
        """
        return self.name


class PastEvent(BaseEvent):
    """
    Model for past events.

    Inherits all fields from BaseEvent.
    Does not add any additional fields or methods.
    Used for events that have already occurred.
    """

    pass


class UpcomingEvent(BaseEvent):
    """
    Model for upcoming events.

    Inherits all fields from BaseEvent and adds:
        - likes: A many-to-many relationship with User to track users
        who liked the event.
    """

    likes = models.ManyToManyField(
        User, related_name="upcoming_event_likes", blank=True
    )


class Comments(models.Model):
    """
    Model for user comments and ratings on past events.

    Fields:
        - user: ForeignKey linking to the User who made the comment.
        - event: ForeignKey linking to the PastEvent the comment is about.
        - review_text: The actual comment or review text.
        - rating: Numerical rating (e.g., 1–5) given to the event.
        - date: Date when the comment was created (auto-filled).
        - time: Time when the comment was created (auto-filled).
    """

    user = models.ForeignKey(
        User, related_name="user", on_delete=models.CASCADE, default=1
    )
    event = models.ForeignKey(
        PastEvent, related_name="comments", on_delete=models.CASCADE
    )
    review_text = models.CharField(max_length=1000)
    rating = models.IntegerField()
    date = models.DateField(auto_now_add=True, null=True, blank=True)
    time = models.TimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        """
        Returns a short description of the review with the event name.
        """
        return f"Review for {self.event.name}"

    def comment(self):
        """
        Returns a string showing the user and event involved in the comment.
        """
        return f"Comment by {self.user.username} on {self.event.name}"


class Likes(models.Model):
    """
    Model to track which users liked which past events.

    Fields:
        - event: ForeignKey to the PastEvent that is liked.
        - user: ForeignKey to the User who liked the event.
    """

    event = models.ForeignKey(PastEvent, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name="likes", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        """
        Returns a string describing who liked which event.
        """
        return f"Like for {self.event.name} by {self.user}"


class Bookings(models.Model):
    """
    Model for booking events.

    Fields:
        - event_name: Name of the event being booked (duplicated,
        not linked to an Event model).
        - user: ForeignKey to the User who made the booking.
        - description: Additional details or notes for the booking.
        - location: Location of the booked event.
        - event_image: Optional image of the event being booked.
        - booking_date: Date of the booking.
        - band_response: Text field storing response from the event
        band/organizer (default = "Pending").
    """

    event_name = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(
        User, related_name="bookings", on_delete=models.CASCADE, null=True, blank=True
    )
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    event_image = models.ImageField(upload_to="event_images/", null=True, blank=True)
    booking_date = models.DateField()
    band_response = models.TextField(null=True, blank=True, default="Pending")

    def __str__(self):
        """
        Returns a summary of the booking showing the
        event name, user, and date.
        """
        return f"""Booking for {self.event_name} by
            {self.user} on {self.booking_date}
            """

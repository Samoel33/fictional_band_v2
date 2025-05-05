from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .forms import UserRegistrationForm


# Create your views here.
def login_user(req):
    """
    View to handle user login.
    This view checks if the request method is POST, and if so,
    it retrieves the username and password from the request.
    It then authenticates the user and logs them in if valid.
    If the user is not valid, it renders the login template
    with an error message.
    If the request method is not POST, it initializes a new form.
    Finally, it renders the login template with the form.

    Args:
        req (object): The request object containing the login data.
        It is used to access the user making the request and
        to render the

    Returns:
        returns the rendered template with the login form.
        If the form is valid, it redirects to the events page.
    """
    form = UserRegistrationForm()
    if req.method == "POST":
        username = req.POST.get("username")
        password = req.POST.get("password1")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(req, user)
            return redirect("/events")
        else:
            context = {"form": form, "error": "Invalid credentials"}
            return render(req, "login.html", context)
    else:
        return render(req, "login.html", {"form": form})


def logout_user(req):
    logout(req)
    return redirect("/")


def register(req):
    """
    View to handle user registration.
    This view checks if the request method is POST, and if so,
    it retrieves the registration data from the request.
    It then validates the form and saves the user if valid.


    Args:
        req (object): The request object containing the
        registration data.
        It is used to access the user making the request and

    Returns:
        returns the rendered template with the registration form.
        If the form is valid, it redirects to the events page.

    """
    if req.method == "POST":
        form = UserRegistrationForm(req.POST)
        if form.is_valid():
            user = form.save()
            login(req, user)
            return redirect("/events")
    else:
        form = UserRegistrationForm()
    return render(req, "register.html", {"form": form})

# Fictional Band App

## 📌 Description

Fictional band application, about the Sam's Band that showcase their journey, awards winnings, previous events, upcoming events and give audience and opportunity to rate and comment their works.

---

## 📚 Table of Contents

- [Description](#-description)
- [Installation](#-installation)
- [Usage](#-usage)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Credits](#-credits)

---

## 🛠 Installation

To install and run this project locally:

1. Clone the repository:

   ```bash
   git clone https://github.com/Samoel33/fictional-band.git
   cd fictional_band
   ```

2. Set up a virtual environment:

   ```bash
   pipenv shell
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   pip install django-boostrap5
   ```

4. Apply migrations:

   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000` to use the app.

---

## ▶️ Usage

Once installed:

- Access the homepage to view your about the band.
- Navigation bar present on every page
- Click “Event” to see Past events.
- Sub navigation in Past event ( click "upcoming events") to see up coming events
- Click "Booking" to book the band for your function or event, Booking
  require user to be logged in.
- Login with credentials if register user, else click "Register" to register in our database.
- If logged in, navigation shows two button left end, click "My Bookings" to view your booking and status.
  -To comment on past Event fill in the form and give rating and click "submit" to save the comment.
  -Click "Like" to Like and event and Click again to remove the like.
- All updates are saved to the local database.

### 📸 Screenshots

> _(Add your own screenshots under a `/screenshots/` folder and reference them here)_

![Home Page](screenshots/Homepage_and_navigation.png)
![Events](screenshots/pastevents.png)
![Upcoming Events](screenshots/Upcoming_events.png)

---

## ✨ Features

- ✅ Register and Login
- ✅ Add Comments and Like Past Events
- ✅ View Past and Upcoming Events
- ✅ Book the Band
- ✅ View Your Bookings and see booking status
- ✅ Mobile-friendly interface using Bootstrap and CSS
- ✅ Local database storage with Django ORM

---

## 🧱 Project Structure

```
Fictional_band/
├── auth_app/
|     ├──templates
├── band_app/
├      ├──templates
├── event_images/
├── fictional_band/
├── static/
├── screenshots/
├── db.sqlite3
├── manage.py
├── Pipfile
├── Pipfile.lock
├── Procfile
└── requirements.txt
```

---

## 🧰 Tech Stack

- Python 3.13
- Django 4.2.20
- SQLite
- HTML5 & CSS3
- Bootstrap 5

---

## 👥 Credits

Project developed by:

- [Samoel Seshoka](https://github.com/Samoel33)

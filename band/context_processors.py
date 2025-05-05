def nav_links(req):
    return {
        "nav_items": [
            {"name": "home", "url": "/"},
            {"name": "events", "url": "/events"},
            {"name": "booking", "url": "/bookings"},
        ]
    }

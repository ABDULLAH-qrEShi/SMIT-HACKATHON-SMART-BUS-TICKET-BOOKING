from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "smartbus-secret-key"

cities = [
    "Karachi",
    "Hyderabad",
    "Sukkur",
    "Mirpur Khas",
    "Lahore"
]

routes = [
    {
        "route_id": "R101",
        "Departure": "Karachi",
        "Destination": "Hyderabad",
        "Departure time": "08:00 AM",
        "Fare": 1200,
        "Total": 40,
        "Availability": 40
    },
    {
        "route_id": "R102",
        "Departure": "Karachi",
        "Destination": "Sukkur",
        "Departure time": "09:30 AM",
        "Fare": 2000,
        "Total": 36,
        "Availability": 36
    },
    {
        "route_id": "R103",
        "Departure": "Hyderabad",
        "Destination": "Mirpur Khas",
        "Departure time": "11:00 AM",
        "Fare": 800,
        "Total": 32,
        "Availability": 32
    },
    {
        "route_id": "R104",
        "Departure": "Karachi",
        "Destination": "Lahore",
        "Departure time": "07:00 PM",
        "Fare": 5000,
        "Total": 45,
        "Availability": 45
    },
    {
        "route_id": "R105",
        "Departure": "Sukkur",
        "Destination": "Hyderabad",
        "Departure time": "02:00 PM",
        "Fare": 1500,
        "Total": 30,
        "Availability": 30
    }
]

bookings = []
next_booking_number = 1001


def find_route(route_id):
    return next(
        (route for route in routes
         if route["route_id"] == route_id),
        None
    )


def generate_report():
    confirmed = [
        b for b in bookings
        if b["status"] == "Confirmed"
    ]

    cancelled = [
        b for b in bookings
        if b["status"] == "Cancelled"
    ]

    return {
        "total_bookings": len(bookings),
        "confirmed_bookings": len(confirmed),
        "cancelled_bookings": len(cancelled),
        "reserved_seats": sum(b["seats"] for b in confirmed),
        "confirmed_revenue": sum(
            b["total_fare"] for b in confirmed
        ),
        "fully_booked_routes": sum(
            route["Availability"] == 0 for route in routes
        )
    }


@app.route("/")
def home():
    view = request.args.get("view", "routes")
    search_term = request.args.get("q", "").strip().lower()
    available_only = request.args.get("available") == "1"

    displayed_routes = [
        route for route in routes
        if (
            not search_term
            or search_term == route["route_id"].lower()
            or search_term in route["Departure"].lower()
            or search_term in route["Destination"].lower()
        )
        and (
            not available_only
            or route["Availability"] > 0
        )
    ]

    schedule = {
        city: [
            route for route in routes
            if route["Departure"] == city
        ]
        for city in cities
    }

    return render_template(
        "index.html",
        view=view,
        routes=routes,
        displayed_routes=displayed_routes,
        bookings=bookings,
        report=generate_report(),
        schedule=schedule,
        search_term=search_term,
        available_only=available_only,
        selected_route=request.args.get("route", "")
    )


@app.route("/book", methods=["POST"])
def book_ticket():
    global next_booking_number

    name = request.form.get("name", "").strip().title()
    route_id = request.form.get("route_id", "").strip().upper()

    try:
        age = int(request.form.get("age", ""))
        seats = int(request.form.get("seats", ""))
    except ValueError:
        flash("Age and seats must be whole numbers.", "error")
        return redirect(url_for("home", view="book"))

    if not name:
        flash("Passenger name is required.", "error")
        return redirect(url_for("home", view="book"))

    if age <= 0:
        flash("Age must be greater than zero.", "error")
        return redirect(url_for("home", view="book"))

    if seats <= 0:
        flash("Seats must be greater than zero.", "error")
        return redirect(url_for("home", view="book"))

    route = find_route(route_id)

    if route is None:
        flash("Route not found.", "error")
        return redirect(url_for("home", view="book"))

    if seats > route["Availability"]:
        flash(
            f"Only {route['Availability']} seats are available.",
            "error"
        )
        return redirect(url_for("home", view="book"))

    booking_id = f"B{next_booking_number}"
    next_booking_number += 1

    booking = {
        "booking_id": booking_id,
        "passenger_name": name,
        "passenger_age": age,
        "route_id": route_id,
        "seats": seats,
        "total_fare": route["Fare"] * seats,
        "status": "Confirmed"
    }

    bookings.append(booking)
    route["Availability"] -= seats

    flash(f"Booking confirmed! ID: {booking_id}", "success")
    return redirect(url_for("home", view="bookings"))


@app.route("/cancel/<booking_id>", methods=["POST"])
def cancel_booking(booking_id):
    booking = next(
        (
            b for b in bookings
            if b["booking_id"] == booking_id.upper()
        ),
        None
    )

    if booking is None:
        flash("Booking ID not found.", "error")

    elif booking["status"] != "Confirmed":
        flash("This booking is already cancelled.", "error")

    else:
        route = find_route(booking["route_id"])

        if route:
            route["Availability"] += booking["seats"]

        booking["status"] = "Cancelled"
        flash("Booking cancelled successfully.", "success")

    return redirect(url_for("home", view="bookings"))


if __name__ == "__main__":
    app.run(debug=True)
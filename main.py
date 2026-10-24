
class Smart_Bus_Ticket:

    def __init__(self):
        self.cities = (
            "Karachi",
            "Hyderabad",
            "Sukkur",
            "Mirpur Khas",
            "Lahore"
        )

        self.routes = [
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

        self.bookings = []
        self.issued_booking_ids = set()
        self.next_booking_number = 1001

    def show_menu(self):
        print("\n" + "=" * 40)
        print("SMART BUS TICKET BOOKING SYSTEM")
        print("=" * 40)
        print("1. View Available Routes")
        print("2. Search for a Route")
        print("3. Book a Ticket")
        print("4. View My Bookings")
        print("5. Cancel a Booking")
        print("6. View Seat Availability")
        print("7. Generate Booking Report")
        print("8. View Route Schedule")
        print("9. Exit")
        print("=" * 40)

    def show_routes(self):
        print("\nAVAILABLE BUS ROUTES")
        print("-" * 75)

        available_only = input(
            "Show only routes with available seats? (y/n): "
        ).strip().lower()

        for index, route in enumerate(self.routes, start=1):

            if available_only == "y" and route["Availability"] == 0:
                continue

            if route["Availability"] == 0:
                status = "Fully Booked"
            else:
                status = "Seats Available"

            print(
                f"{index}. {route['route_id']} | "
                f"{route['Departure']} -> "
                f"{route['Destination']} | "
                f"{route['Departure time']} | "
                f"Rs. {route['Fare']} | "
                f"Seats: {route['Availability']}/{route['Total']} | "
                f"{status}"
            )

    def search_route(self):
        print("\nSEARCH FOR A ROUTE")

        search_term = input(
            "Enter route ID  "
        ).strip().lower()

        if not search_term:
            print("Search input cannot be empty.")
            return

        found = False

        for route in self.routes:
            if route["route_id"].lower() == search_term:
                print(
                    f"{route['route_id']} | "
                    f"{route['Departure']} -> "
                    f"{route['Destination']} | "
                    f"{route['Departure time']} | "
                    f"Rs. {route['Fare']} | "
                    f"Seats: {route['Availability']}/{route['Total']}"
                )
                found = True
                break

        else:
            for route in self.routes:
                if (
                    route["Departure"].lower() == search_term
                    or route["Destination"].lower() == search_term
                ):
                    print(
                        f"{route['route_id']} | "
                        f"{route['Departure']} -> "
                        f"{route['Destination']} | "
                        f"{route['Departure time']} | "
                        f"Rs. {route['Fare']} | "
                        f"Seats: {route['Availability']}/{route['Total']}"
                    )
                    found = True

            if not found:
                print("No matching route found.")

    def book_ticket(self):
        print("\n" + "=" * 40)
        print("BOOK A TICKET")
        print("=" * 40)

        name = input("Enter your name: ").strip().title()

        if not name:
            print("The name section cannot be left empty.")
            return

        try:
            age = int(input("Enter your age: "))

            if age <= 0:
                print("Age must be greater than zero.")
                return

            seats = int(input("Enter the number of seats to book: "))

            if seats <= 0:
                print("Seats must be greater than zero.")
                return

        except ValueError:
            print("Age and seats must be whole numbers.")
            return

        route_id = input("Enter route ID: ").strip().upper()
        selected_route = None

        for route in self.routes:
            if route["route_id"] == route_id:
                selected_route = route
                break

        else:
            print("Route not found.")
            return

        if seats > selected_route["Availability"]:
            print("Not enough seats available.")
            print("Seats remaining:", selected_route["Availability"])
            return

        booking_id = f"B{self.next_booking_number}"

        while booking_id in self.issued_booking_ids:
            self.next_booking_number += 1
            booking_id = f"B{self.next_booking_number}"

        self.next_booking_number += 1

        total_fare = selected_route["Fare"] * seats

        booking = {
            "booking_id": booking_id,
            "passenger_name": name,
            "passenger_age": age,
            "route_id": route_id,
            "seats": seats,
            "total_fare": total_fare,
            "status": "Confirmed"
        }

        self.bookings.append(booking)
        self.issued_booking_ids.add(booking_id)
        selected_route["Availability"] -= seats

        print("\nBooking confirmed!")
        print("Booking ID:", booking_id)
        print("Passenger:", name)
        print("Age:", age)
        print(
            "Route:",
            selected_route["Departure"],
            "->",
            selected_route["Destination"]
        )
        print("Seats booked:", seats)
        print("Fare per seat: Rs.", selected_route["Fare"])
        print("Total fare: Rs.", total_fare)
        print("Status: Confirmed")

    def my_bookings(self):
        print("\n" + "=" * 40)
        print("MY BOOKINGS")
        print("=" * 40)

        if not self.bookings:
            print("No bookings found.")
            return

        for index, booking in enumerate(self.bookings, start=1):
            print(f"\nBooking {index}")
            print("Booking ID:", booking["booking_id"])
            print("Passenger:", booking["passenger_name"])
            print("Age:", booking["passenger_age"])
            print("Route ID:", booking["route_id"])
            print("Seats:", booking["seats"])
            print("Total Fare: Rs.", booking["total_fare"])
            print("Status:", booking["status"])

    def cancel_booking(self):
        print("\n" + "=" * 40)
        print("CANCEL BOOKING")
        print("=" * 40)

        cancel_id = input("Enter Booking ID: ").strip().upper()

        for booking in self.bookings:
            if cancel_id == booking["booking_id"]:

                if booking["status"] != "Confirmed":
                    print("This booking has already been cancelled.")
                    return

                for route in self.routes:
                    if route["route_id"] == booking["route_id"]:
                        route["Availability"] += booking["seats"]
                        break

                booking["status"] = "Cancelled"

                print(f"Booking {cancel_id} cancelled successfully!")
                print("Seats restored:", booking["seats"])
                return

        print("Booking ID not found.")

    def view_available_seats(self):
        print("\n" + "=" * 40)
        print("SEAT AVAILABILITY")
        print("=" * 40)

        available_only = input(
            "Show only routes with seats available? (y/n): "
        ).strip().lower()

        for index, route in enumerate(self.routes, start=1):

            if available_only == "y" and route["Availability"] == 0:
                continue

            if route["Availability"] == route["Total"]:
                status = "Available"
            elif route["Availability"] == 0:
                status = "Fully Booked"
            else:
                status = "Partially Booked"

            print(
                f"{index}. {route['route_id']} | "
                f"{route['Departure']} -> {route['Destination']} | "
                f"Seats: {route['Availability']}/{route['Total']} | "
                f"{status}"
            )

    def booking_report(self):
        print("\n" + "=" * 40)
        print("BOOKING REPORT")
        print("=" * 40)

        total_bookings = len(self.bookings)
        confirmed_bookings = 0
        cancelled_bookings = 0
        reserved_seats = 0
        confirmed_revenue = 0
        fully_booked_routes = 0

        for booking in self.bookings:
            if booking["status"] == "Confirmed":
                confirmed_bookings += 1
            elif booking["status"] == "Cancelled":
                cancelled_bookings += 1

        for route in self.routes:
            route_reserved_seats = 0
            route_revenue = 0

            for booking in self.bookings:
                if (
                    booking["route_id"] == route["route_id"]
                    and booking["status"] == "Confirmed"
                ):
                    route_reserved_seats += booking["seats"]
                    route_revenue += booking["total_fare"]

            reserved_seats += route_reserved_seats
            confirmed_revenue += route_revenue

            if route["Availability"] == 0:
                fully_booked_routes += 1

        print("Total bookings created:", total_bookings)
        print("Confirmed bookings:", confirmed_bookings)
        print("Cancelled bookings:", cancelled_bookings)
        print("Seats currently reserved:", reserved_seats)
        print("Confirmed revenue: Rs.", confirmed_revenue)
        print("Fully booked routes:", fully_booked_routes)

    def route_schedule(self):
        print("\n" + "=" * 40)
        print("ROUTE SCHEDULE BY DEPARTURE CITY")
        print("=" * 40)

        for city in self.cities:
            print(f"\n{city}")

            found = False

            for route in self.routes:
                if route["Departure"] == city:
                    print(
                        f"  {route['route_id']} -> "
                        f"{route['Destination']} | "
                        f"{route['Departure time']}"
                    )
                    found = True

            if not found:
                print("  No scheduled departures.")

    def main(self):
        while True:
            self.show_menu()
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.show_routes()

            elif choice == "2":
                self.search_route()

            elif choice == "3":
                self.book_ticket()

            elif choice == "4":
                self.my_bookings()

            elif choice == "5":
                self.cancel_booking()

            elif choice == "6":
                self.view_available_seats()

            elif choice == "7":
                self.booking_report()

            elif choice == "8":
                self.route_schedule()

            elif choice == "9":
                print("Thank you for using Smart Bus!")
                break

            else:
                print("Invalid input. Enter a number from 1 to 9.")


if __name__ == "__main__":
    bus = Smart_Bus_Ticket()
    bus.main()

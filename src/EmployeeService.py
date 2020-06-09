from getpass import getpass
from datetime import datetime, date

from src.EmployeeRepository import EmployeeRepository


class Employee:

    def __init__(self):
        self.employee_id = None
        self.employee_repository = EmployeeRepository()

    def employee_login(self):
        """
        employee authentication.
        :return:
        """
        email = input("Enter Email Id: ")
        employee = self.employee_repository.employee_login(email)

        if employee:
            if employee[1] is None:
                password = getpass('First time Login. Enter Password: ')
                self.employee_repository.set_password(password, employee[2])
                self.employee_id = employee[2]
                return True
            else:
                password = getpass('Enter Password: ')
                if employee[1] == password:
                    print("Authentication Successful")
                    self.employee_id = employee[2]
                    return True
                else:
                    print("Authentication failed. Please check your credentials")
                    return False
        else:
            print("User does not exist")
            return False

    def employee_tasks(self):
        """
        show employee tasks.
        :return:
        """
        option = ''
        while option != '5':
            print("\nMenu\n"
                  "1: Book cab\n"
                  "2: Show Past Bookings\n"
                  "3: Show Upcoming Bookings\n"
                  "4: Cancel Booking\n"
                  "5: Exit\n")
            option = input("Select option: ")
            if option == '1':
                self.book_cab()
            elif option == '2':
                self.show_past_bookings()
            elif option == '3':
                self.show_upcoming_bookings()
            elif option == '4':
                self.cancel_booking()
            elif option == '5':
                print("Thank You")
            else:
                print("Invalid choice.")

    def show_past_bookings(self):
        """
        show past booking details.
        :return:
        """
        try:
            bookings = self.employee_repository.show_past_bookings(self.employee_id)
            if bookings:
                for booking in bookings:
                    print("Booking Id : {}".format(booking[5]))
                    print("Date : {}".format(booking[0]))
                    print("Pick up time : {}".format(booking[1]))
                    print("Cab_Number : {}".format(booking[2]))
                    print("Pick up location: {}".format(booking[3]))
                    print("Destination : {}".format(booking[4]))
                    print("----------------------------")
                return True
            else:
                print("No bookings found.")
                return False
        except Exception as e:
            print("Some Error occurred.")
            return False

    def show_upcoming_bookings(self):
        """
        show upcoming booking details.
        :return:
        """
        try:
            bookings = self.employee_repository.show_upcoming_bookings(self.employee_id)
            if bookings:
                for booking in bookings:
                    print("Booking Id : {}".format(booking[5]))
                    print("Date : {}".format(booking[0]))
                    print("Pick up time : {}".format(booking[1]))
                    print("Cab_Number : {}".format(booking[2]))
                    print("Pick up location: {}".format(booking[3]))
                    print("Destination : {}".format(booking[4]))
                    print("----------------------------")
                return True
            else:
                print("No bookings found.")
                return False
        except Exception as e:
            print("Some Error occurred.")
            return False

    def show_all_routes(self):
        """
        show details of all routes.
        :return:
        """
        try:
            routes = self.employee_repository.show_all_routes()
            if routes:
                print("\nAvailable Routes: \n")
                for route in routes:
                    print("Route Id: {}".format(route[0]))
                    print("Route : {}".format(route[1]))
                    print("----------------------------")
                return True
            else:
                print("No records found.")
                return False
        except Exception as e:
            print("Some Error occurred.Please try again")
            return False

    def check_availability(self, route_id, source, destination, timings):
        """
        check availability of cabs.
        """
        bookings = self.employee_repository.check_availability(route_id, source, destination, timings)
        if bookings:
            print("All Available Cabs after {}: \n".format(timings))
            for booking in bookings:
                print('''Cab Number: {}\nTimings: {}\nSeats Available: {}\n
                          '''.format(booking[0], booking[1], booking[2]))
            return True
        else:
            print("No cabs available")
            return False

    def book_cab(self):
        """
        book a cab.
        :return:
        """
        try:
            self.show_all_routes()
            route_id = input("Enter your Route Id: ")
            source = input("Enter Pick up location: ")
            destination = input("Enter Destination: ")
            timings = input("Enter Timings (list all available cabs after this time) in HH:SS format: ")
            if self.check_availability(route_id, source, destination, timings):
                cab_num = input("Enter the vehicle number of the cab you want to book: ")
                time = input("Enter pickup time as per cab timings in HH:SS format: ")
                self.employee_repository.book_cab(self.employee_id, route_id, cab_num, source, destination, time)
                print("Cab booked successfully! Cab Number: {}".format(cab_num))
                self.decrement_seats(cab_num, route_id, source, destination, time)
                return True
            else:
                return False
        except Exception as e:
            print("Some Error occurred.")
            return False

    def decrement_seats(self, cab_num, route_id, source, destination, time):
        """
        reduce the number of seats in a cab.
        :return:
        """
        try:
            self.employee_repository.decrement_seats(cab_num, route_id, source, destination, time)
            return True
        except Exception as e:
            print("Some Error occurred.")
            return False

    def increment_seats(self, cab_num, route_id, source, destination, time):
        """
        increase the number of seats in a cab.
        :return:
        """
        try:
            self.employee_repository.increment_seats(cab_num, route_id, source, destination, time)
            return True
        except Exception as e:
            print("Some Error occurred.")
            return False

    def cancel_booking(self):
        """
        cancel a booking.
        :return:
        """
        try:
            if self.show_upcoming_bookings():
                booking_id = int(input("Enter Booking Id of the ride you want to cancel: "))
                booking = self.get_booking_by_id(booking_id)
                if booking:
                    pickup_time = datetime.strptime(booking[1], '%H:%M').time()
                    booking_date = datetime.strptime(booking[0], '%Y-%m-%d').date()
                    difference = datetime.combine(booking_date, pickup_time) - datetime.combine(date.today(),
                                                                                                datetime.now().time())
                    if (difference.total_seconds() / 60) > 30:
                        self.employee_repository.cancel_booking(booking_id)
                        print("Booking cancelled successfully.")
                        self.increment_seats(booking[2], booking[3], booking[4], booking[5], booking[1])
                        return True
                    else:
                        print("Booking Cancellation Failed. Cancellations should be done 30 mins prior to the scheduled time.")
                        return False
                else:
                    print("No records found.")
                    return False
            else:
                return False
        except Exception as e:
            print("Some Error occurred.")
            return False

    def get_booking_by_id(self, booking_id):
        """
        show booking details by booking id.
        :return:
        """
        try:
            booking = self.employee_repository.get_booking_by_id(booking_id)
            if booking:
                return booking
            else:
                print("Invalid Booking Id.")
                return False
        except Exception as e:
            print("Some Error occurred.")
            return False

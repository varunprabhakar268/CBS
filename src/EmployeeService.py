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
        record = self.employee_repository.employee_login(email)

        if record:
            if record[1] is None:
                password = getpass('First time Login. Enter Password: ')
                self.employee_repository.set_password(password, record[2])
                self.employee_id = record[2]
                return True
            else:
                password = getpass('Enter Password: ')
                if record[1] == password:
                    print("Authentication Successful")
                    self.employee_id = record[2]
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
            result = self.employee_repository.show_past_bookings(self.employee_id)

            if result:
                for i in result:
                    print("Booking Id : {}".format(i[5]))
                    print("Date : {}".format(i[0]))
                    print("Pick up time : {}".format(i[1]))
                    print("Cab_Number : {}".format(i[2]))
                    print("Pick up location: {}".format(i[3]))
                    print("Destination : {}".format(i[4]))
                    print("----------------------------")
                return True
            else:
                print("No records found.")
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
            result = self.employee_repository.show_upcoming_bookings(self.employee_id)

            if result:
                for i in result:
                    print("Booking Id : {}".format(i[5]))
                    print("Date : {}".format(i[0]))
                    print("Pick up time : {}".format(i[1]))
                    print("Cab_Number : {}".format(i[2]))
                    print("Pick up location: {}".format(i[3]))
                    print("Destination : {}".format(i[4]))
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
            result = self.employee_repository.show_all_routes()

            if result:
                print("\nAvailable Routes: \n")
                for i in result:
                    print("Route Id: {}".format(i[0]))
                    print("Route : {}".format(i[1]))
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
        records = self.employee_repository.check_availability(route_id, source, destination, timings)

        print(records)
        if records:
            print("All Available Cabs after {}: \n".format(timings))
            for record in records:
                print('''Cab Number: {}\nTimings: {}\nSeats Available: {}\n
                          '''.format(record[0], record[1], record[2]))
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
                record = self.get_booking_by_id(booking_id)
                if len(record) != 0:
                    pickup_time = datetime.strptime(record[1], '%H:%M').time()
                    booking_date = datetime.strptime(record[0], '%Y-%m-%d').date()
                    difference = datetime.combine(booking_date, pickup_time) - datetime.combine(date.today(),
                                                                                                datetime.now().time())
                    if (difference.total_seconds() / 60) > 30:
                        self.employee_repository.cancel_booking(booking_id)

                        print("Booking cancelled successfully.")
                        self.increment_seats(record[2], record[3], record[4], record[5], record[1])
                        return True
                    else:
                        print(
                            "Booking Cancellation Failed. Cancellations should be done 30 mins prior to the scheduled time.")
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
            result = self.employee_repository.get_booking_by_id(booking_id)
            if result:
                return result

        except Exception as e:
            print("Some Error occurred.")
            return False

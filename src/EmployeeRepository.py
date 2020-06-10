from src import DbConnection


class EmployeeRepository:
    def __init__(self):
        self.conn = DbConnection.create_connection()

    def employee_login(self, email):
        sql = "SELECT email,password,id FROM Employees WHERE email = '{}'".format(email)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchone()

    def set_password(self, password, id):
        sql = "Update Employees SET password = '{}' WHERE id = {}".format(password, id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)

    def show_past_bookings(self, employee_id):
        sql = """ select date(created_at),timings,cab_number,source,destination,id from bookings 
                              where date(created_at) <= date('now','localtime') and 
                              timings <= time('now','localtime') and 
                              cancelled = 'no' and emp_id = {}
                          """.format(employee_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchall()

    def show_upcoming_bookings(self, employee_id):
        sql = """ select date(created_at),timings,cab_number,source,destination,id from bookings 
                              where date(created_at) >= date('now','localtime') and 
                              timings >= time('now','localtime') and 
                              cancelled = 'no' and emp_id = {}
                          """.format(employee_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchall()

    def show_all_routes(self):
        sql = "select * from Routes"
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchall()

    def check_availability(self, route_id, source, destination, timings):
        sql = '''select cab_number,timings,seats_available,stop_name,stop_stage from cab_routes 
                         where stop_name = "{}" and  route_id = "{}" and seats_available !=0 and timings > "{}" and timings > time('now','localtime') 
                         and stop_stage < (select stop_stage from cab_routes where stop_name = "{}" and route_id = "{}")        
                '''.format(source, route_id, timings, destination, route_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchall()

    def book_cab(self, booking):
        sql = """INSERT INTO Bookings (emp_id,route_id,cab_number,source,destination,timings)
                                 VALUES ({},'{}','{}','{}','{}','{}')
                              """.format(booking.emp_id, booking.route_id, booking.cab_number, booking.source, booking.destination, booking.timings)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()

    def decrement_seats(self, cab_num, route_id, source, destination, time):
        sql = '''
                    Update cab_routes Set seats_available = seats_available - 1 
                    where cab_number = "{}" and route_id = "{}" and timings = "{}" and
                    stop_stage between 
                    (select stop_stage from cab_routes where cab_number = "{}" and stop_name = "{}" 
                    and  route_id = "{}" and timings = "{}") 
                    and 
                    (select stop_stage from cab_routes where cab_number = "{}" and stop_name = "{}" 
                    and  route_id = "{}" and timings = "{}")
              '''.format(cab_num, route_id, time, cab_num, source, route_id, time, cab_num, destination, route_id, time)

        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()

    def increment_seats(self, cab_num, route_id, source, destination, time):
        sql = '''
                    Update cab_routes Set seats_available = seats_available + 1 
                    where cab_number = "{}" and route_id = "{}" and timings = "{}" and
                    stop_stage between 
                    (select stop_stage from cab_routes where cab_number = "{}" and stop_name = "{}" 
                    and  route_id = "{}" and timings = "{}") 
                    and 
                    (select stop_stage from cab_routes where cab_number = "{}" and stop_name = "{}" 
                    and  route_id = "{}" and timings = "{}")
                '''.format(cab_num, route_id, time, cab_num, source, route_id, time, cab_num, destination, route_id,
                           time)

        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()

    def cancel_booking(self, booking_id):
        sql = '''Update Bookings set cancelled = "yes" where id = {}'''.format(booking_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()

    def get_booking_by_id(self, booking_id):
        sql = """ select date(created_at),timings,cab_number,route_id,source,destination from bookings where id = {}
              """.format(booking_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchone()

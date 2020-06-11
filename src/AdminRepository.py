from src import DbConnection


class AdminRepository:
    def __init__(self):
        self.conn = DbConnection.create_connection()

    def admin_login(self,email):
        sql = "SELECT email,password,id FROM Admin WHERE email = '{}'".format(email)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchone()

    def create_employee(self, employee):
        sql = "INSERT INTO Employees (name,email) VALUES ('{}','{}')".format(employee.name, employee.email)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)

    def get_employee_by_id(self, employee_id):
        sql = "SELECT name,email FROM Employees WHERE id = {}".format(employee_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchone()

    def update_employee(self,name, email, employee_id):
        sql = ''' UPDATE Employees
                  SET name = '{}',
                  email = '{}'                    
                  WHERE id = {}
              '''.format(name, email, employee_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()

    def delete_employee(self,employee_id):
        sql = 'DELETE FROM Employees WHERE id={}'.format(employee_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)

    def show_all_employees(self):
        sql = "select * from Employees"
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchall()

    def create_cab(self,cab):
        sql = """INSERT INTO Cabs (cab_number,capacity)
                 VALUES ('{}',{})
              """.format(cab.cab_number, cab.capacity)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)

    def create_route(self,route):
        sql = """
                INSERT INTO Routes (route)
                VALUES ('{}')
              """.format(route.route)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)

    def get_cab_by_id(self, cab_num):
        sql = "SELECT cab_number,capacity FROM Cabs WHERE cab_number = '{}'".format(cab_num)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchone()

    def get_route_by_id(self, route_id):
        sql = "SELECT * FROM Routes WHERE route_id = {}".format(route_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchone()

    def update_cab(self,capacity, cab_num):
        sql = ''' UPDATE Cabs
                  SET capacity = {}                   
                  WHERE cab_number = "{}" 
              '''.format(capacity, cab_num)

        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()

    def delete_cab(self,cab_num):
        sql = 'DELETE FROM Cabs WHERE cab_number="{}"'.format(cab_num)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)

    def delete_route(self,route_id):
        sql = 'DELETE FROM Routes WHERE route_id={}'.format(route_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)

    def show_all_cabs(self):
        sql = "select cab_number,capacity from Cabs"
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

    def create_cab_route(self,cab_route):
        sql = """Insert into cab_routes(cab_number,route_id,stop_name,stop_stage,timings)
                 Values('{}','{}','{}',{},'{}')
              """.format(cab_route.cab_number,cab_route.route_id,cab_route.stop_name,cab_route.stop_stage,cab_route.timings)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)

    def get_cab_route_by_cab_num(self, cab_num):
        sql = '''SELECT id,cab_number,route_id,stop_name,stop_stage,timings FROM cab_routes 
                 WHERE cab_number = "{}" '''.format(cab_num)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchall()

    def get_all_cab_routes(self):
        sql = '''SELECT id,cab_number,route_id,stop_name,stop_stage,timings FROM cab_routes'''
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchall()

    def get_cab_route_by_id(self, id):
        sql = '''SELECT id,cab_number,route_id,stop_name,stop_stage,timings FROM cab_routes 
                 WHERE id = {} '''.format(id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchone()

    def update_cab_route(self,updated_cab_num, route_id, stop_name, stop_stage, timings, id):
        sql = ''' UPDATE cab_routes
                  SET cab_number = '{}' ,
                  route_id = '{}' ,
                  stop_name = '{}',
                  stop_stage = {},
                  timings = '{}'
                  WHERE id = {}'''.format(updated_cab_num, route_id, stop_name, stop_stage, timings,id)

        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()

    def delete_cab_route(self,cab_num, route_id):
        sql = 'DELETE FROM cab_routes WHERE cab_number="{}" and route_id = "{}"'.format(cab_num, route_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()

    def show_emp_bookings(self,emp_id):
        sql = """ select date(created_at),timings,cab_number,source,destination,id from bookings 
                  where cancelled = 'no' and emp_id = {}
              """.format(emp_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchall()

    def show_total_bookings_day(self, booking_date):
        sql = """select date(created_at) as 'Date', count(*) as 'TotalBookings'  from bookings 
                 where date(created_at) = '{}' and cancelled = 'no' group by date(created_at)
              """.format(booking_date)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchone()

    def show_total_bookings_week(self,booking_week):
        sql = """select  strftime('%W',date(created_at)) as week_number , count(*) as 'TotalBookings'  from bookings
                 where strftime('%W',date(created_at)) = '{}' and cancelled = 'no' 
                 group by strftime('%W',date(created_at))
              """.format(booking_week)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchone()

    def show_total_bookings_month(self, booking_month):
        sql = """select  strftime('%m',date(created_at)) as 'Month' , count(*) as 'TotalBookings'  from bookings 
                 where strftime('%m',date(created_at)) = '{}' and cancelled = 'no'
                 group by strftime('%m',date(created_at))
              """.format(booking_month)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchone()





def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''
             CREATE TABLE IF NOT EXISTS Admin
             (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(30)    NOT NULL,
                email VARCHAR(30)    NOT NULL unique,
                password VARCHAR(20) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
             );''')
    conn.commit()

    # cursor.execute("INSERT INTO Admin(name,email,password) VALUES ('captain','cap@gmail.com','password');")
    # conn.commit()

    cursor.execute('''
             CREATE TABLE IF NOT EXISTS Employees
             (
                id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                name VARCHAR(30) NOT NULL,
                email VARCHAR(30)    NOT NULL UNIQUE,
                password VARCHAR(20),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
             );''')
    conn.commit()

    cursor.execute('''
             CREATE TABLE IF NOT EXISTS Cabs
             (
                cab_number VARCHAR(20) NOT NULL PRIMARY KEY UNIQUE,
                capacity INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
             );
             ''')
    conn.commit()

    cursor.execute('''
             CREATE TABLE IF NOT EXISTS cab_routes
             (
                id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                cab_number VARCHAR(30) NOT NULL,
                route_id VARCHAR(30) NOT NULL,
                stop_name VARCHAR(30) NOT NULL,
                stop_stage INTEGER   NOT NULL,
                seats_available   INTEGER(10),
                timings TIME NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cab_number) REFERENCES Cabs(cab_number) ON DELETE CASCADE
             );''')
    conn.commit()

    cursor.execute('''
             CREATE TRIGGER IF NOT EXISTS 'cab_routes_seats_available_val'
             After INSERT ON cab_routes
             WHEN new.seats_available IS NULL
             BEGIN
             UPDATE cab_routes
             SET 
             seats_available = (SELECT capacity FROM Cabs Where Cabs.cab_number = new.cab_number)
             WHERE
             cab_number = new.cab_number;
             END;''')
    conn.commit()

    cursor.execute('''
             CREATE TABLE IF NOT EXISTS Bookings
             (
                id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                emp_id           INTEGER(10) NOT NULL,
                route_id           VARCHAR(10)    NOT NULL,
                cab_number        VARCHAR(50) NOT NULL,
                source        VARCHAR(50) NOT NULL,
                destination        VARCHAR(50) NOT NULL,
                timings       TIME,
                cancelled VARCHAR(50) DEFAULT "no",
                created_at DATETIME DEFAULT (datetime('now','localtime')),
                FOREIGN KEY (route_id) REFERENCES Routes(route_id) ON DELETE CASCADE,
                FOREIGN KEY (emp_id) REFERENCES Employees(id) ON DELETE CASCADE,
                FOREIGN KEY (cab_number) REFERENCES Cabs(cab_number)ON DELETE CASCADE
             );''')
    conn.commit()

    cursor.execute('''
             CREATE TABLE IF NOT EXISTS Routes
             (
                route_id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                route           VARCHAR(1000) NOT NULL
             );''')

    conn.commit()

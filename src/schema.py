def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Admin
             (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
             name VARCHAR(30)    NOT NULL,
             email VARCHAR(30)    NOT NULL unique,
             password VARCHAR(20) NOT NULL,
             created_at DATETIME DEFAULT CURRENT_TIMESTAMP);''')
    conn.commit()

    # cursor.execute("INSERT INTO Admin(name,email,password) VALUES ('captain','captain@gmail.com','password');")
    # conn.commit()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Employees
             (id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
             name VARCHAR(30) NOT NULL,
             email VARCHAR(30)    NOT NULL UNIQUE,
             password VARCHAR(20),
             role VARCHAR(10) DEFAULT "none",
             created_at DATETIME DEFAULT CURRENT_TIMESTAMP);''')
    conn.commit()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Supervisors
             (id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
             name VARCHAR(30) NOT NULL,
             email VARCHAR(20)    NOT NULL,
             password VARCHAR(20),
             assigned VARCHAR(20)    DEFAULT "no",
             TeamName Varchar(20) NOT NULL,
             created_at DATETIME DEFAULT CURRENT_TIMESTAMP);''')
    conn.commit()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Complaints
             (id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
             accident_name           VARCHAR(30) NOT NULL,
             comments           VARCHAR(50)    NOT NULL,
             worker_id        INTEGER(10) NOT NULL,
             status             VARCHAR(10) DEFAULT "open",
             assigned_team      Varchar(20) DEFAULT "none",
             created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (worker_id) REFERENCES Employees(id) ON DELETE CASCADE,
            FOREIGN KEY (assigned_team) REFERENCES Supervisors(TeamName) ON DELETE CASCADE);''')
    conn.commit()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Report
             (id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
             complaint_id           INTEGER(10) NOT NULL,
             TeamName           VARCHAR(10)    NOT NULL,
             root_cause        VARCHAR(50) NOT NULL,
             details             VARCHAR(100) NOT NULL,
             no_of_people_affected INTERGER NOT NULL,
             no_of_casualties INTEGRER NOT NULL,
             status             VARCHAR(10)  DEFAULT "none",
             created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (complaint_id) REFERENCES Complaints(id) ON DELETE CASCADE,
            FOREIGN KEY (TeamName) REFERENCES Supervisors(TeamName)ON DELETE CASCADE);''')
    conn.commit()
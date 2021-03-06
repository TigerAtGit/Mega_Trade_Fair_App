import mysql.connector as mysql

class servicesdb:
    def __init__(self):
        self.connector = None
        self.dbcursor = None
        self.connect_database()
        self.create_table()
    
    def connect_database(self):
        self.connector = mysql.connect(host='127.0.0.1', user='root', password='Urmil@2000')

        self.dbcursor = self.connector.cursor()
        self.dbcursor.execute('CREATE DATABASE IF NOT EXISTS MegaTradeFair')
        self.dbcursor.execute('USE MegaTradeFair')
        #self.dbcursor.execute('USE test')

    def create_table(self):
        self.dbcursor.execute(''' CREATE TABLE IF NOT EXISTS Country(
        Id INT NOT NULL AUTO_INCREMENT,
        CountryName VARCHAR(200),
        PRIMARY KEY (id)
        );''')

        self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS State(
            Id INT NOT NULL AUTO_INCREMENT,
            StateName VARCHAR(200),
            Country_id INT,
            PRIMARY KEY (id),
            FOREIGN KEY (country_id) REFERENCES Country(id) ON UPDATE CASCADE ON DELETE CASCADE
        ); ''')

        self.dbcursor.execute('''CREATE TABLE if NOT EXISTS Industry(
            Id INT NOT NULL AUTO_INCREMENT,
            IndustryName VARCHAR(200),
            PRIMARY KEY (id)
        ); ''')

        self.dbcursor.execute('''CREATE TABLE if NOT EXISTS Venue(
            Id INT NOT NULL AUTO_INCREMENT,
            City VARCHAR(200),
            Address VARCHAR(200),
            Country_id INT,
            State_id INT,
            PRIMARY KEY (Id),
            FOREIGN KEY (Country_id) REFERENCES Country(Id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (State_id) REFERENCES State(Id) ON UPDATE CASCADE ON DELETE CASCADE
        ); ''')

        self.dbcursor.execute('''CREATE TABLE if NOT EXISTS Event(
            Id INT NOT NULL AUTO_INCREMENT,
            Name VARCHAR(200),
            BookingStartDate DATETIME NOT NULL,
            StartDate DATETIME NOT NULL,
            EndDate DATETIME NOT NULL,
            Venue_Id INT,
            PRIMARY KEY (Id),
            FOREIGN KEY (Venue_Id) REFERENCES Venue(Id) ON UPDATE CASCADE ON DELETE CASCADE
        ); ''')

        self.dbcursor.execute('''CREATE TABLE if NOT EXISTS Stall(
            Id INT NOT NULL AUTO_INCREMENT,
            StallNo INT NOT NULL,
            Price FLOAT NOT NULL,
            StallSize INT,
            IsBooked BIT NOT NULL,
            Event_Id INT,
            PRIMARY KEY (Id),
            FOREIGN KEY (Event_Id) REFERENCES Event(Id) ON DELETE CASCADE ON UPDATE CASCADE
        ); ''')

        self.dbcursor.execute('''CREATE TABLE if NOT EXISTS Visitor(
            Id INT NOT NULL AUTO_INCREMENT,
            FirstName VARCHAR(30),
            LastName VARCHAR(30),
            Address VARCHAR(200),
            Pincode INT NOT NULL,
            MobileNo VARCHAR(10) NOT NULL,
            EmailId VARCHAR(100) NOT NULL,
            DateOfBirth DATETIME,
            Gender BIT NOT NULL,
            PRIMARY KEY (Id)
        ); ''')

        self.dbcursor.execute('''CREATE TABLE if NOT EXISTS Exhibitor(
            Id INT NOT NULL AUTO_INCREMENT,
            ExhibitorName VARCHAR(30),
            EmailId VARCHAR(100),
            PhoneNo VARCHAR(10),
            CompanyName VARCHAR(200),
            CompanyDescription VARCHAR(300),
            Address VARCHAR(200),
            Pincode INT NOT NULL,
            Industry_Id INT,
            Country_Id INT,
            State_Id INT,
            PRIMARY KEY (Id),
            FOREIGN KEY (Industry_Id) REFERENCES Industry(Id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (Country_Id) REFERENCES Country(Id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (State_Id) REFERENCES State(Id) ON UPDATE CASCADE ON DELETE CASCADE
        ); ''')

        self.dbcursor.execute('''CREATE TABLE if NOT EXISTS Booking(
            Id INT NOT NULL AUTO_INCREMENT,
            BookingDate DATETIME NOT NULL,
            TotalAmount FLOAT NOT NULL,
            Event_Id INT,
            Exhibitor_Id INT,
            PRIMARY KEY (Id),
            FOREIGN KEY (Event_Id) REFERENCES Event(Id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (Exhibitor_Id) REFERENCES Exhibitor(Id) ON UPDATE CASCADE ON DELETE CASCADE
        ); ''')

        self.dbcursor.execute('''CREATE TABLE if NOT EXISTS BookingStallMap(
            Id INT NOT NULL AUTO_INCREMENT,
            Booking_Id INT,
            Event_Id INT,
            Stall_Id INT,
            PRIMARY KEY (Id),
            FOREIGN KEY (Event_Id) REFERENCES Event(Id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (Stall_Id) REFERENCES Stall(Id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (Booking_Id) REFERENCES Booking(Id) ON UPDATE CASCADE ON DELETE CASCADE
        ); ''')

        self.dbcursor.execute('''CREATE TABLE if NOT EXISTS MegaConsumerCard(
            Id INT NOT NULL AUTO_INCREMENT,
            Spend INT NOT NULL,
            SpendDate DATETIME NOT NULL,
            PaymentMode VARCHAR(200),
            
            Event_Id INT,
            Booking_Id INT,
            Visitor_Id INT,
            PRIMARY KEY (Id),
            FOREIGN KEY (Event_Id) REFERENCES Event(Id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (Booking_Id) REFERENCES Booking(Id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (Visitor_Id) REFERENCES Visitor(Id) ON UPDATE CASCADE ON DELETE CASCADE	
        );''')

        self.connector.commit()

    def add_record(self, table_name, input_data):
        keys = list(input_data.keys())
        
        #Preparing Query
        table_data, table_values = '(', ' VALUES ('
        for i, x in enumerate(keys):
            if i != len(keys)-1:
                table_values += f'%({x})s, '
                table_data += f'{x}, '
            else:
                table_values += f'%({x})s)'
                table_data += f'{x})'

        add_query = (f'INSERT INTO {table_name} ' + table_data + table_values)
        print(add_query)

        #Execute Query
        try:
            self.dbcursor.execute(add_query, input_data)
            self.connector.commit()
        except Exception as e:
            print(e)

    def fetch_records(self, table_name):
        select_query = (f'SELECT * FROM {table_name}')

        self.dbcursor.execute(select_query)
        records = self.dbcursor.fetchall()
        return records

    def retrieve_industry_bookings(self, industry_name):
        records = []

        industry_booking_query = (''' SELECT t1.Event_Id, t5.StallNo, t2.ExhibitorName, t2.CompanyName, t3.IndustryName, t1.TotalAmount, t1.BookingDate 
                            FROM booking AS t1
                            JOIN exhibitor AS t2 ON t1.Exhibitor_Id = t2.Id
                            JOIN bookingstallmap AS t4 ON t4.Booking_Id = t1.Id
                            JOIN stall AS t5 ON t5.Id = t4.Stall_Id
                            JOIN industry AS t3 ON t2.Industry_Id = t3.Id WHERE t3.IndustryName = %(IndustryName)s
                            ORDER BY t1.Event_Id ASC''')

        self.dbcursor.execute(industry_booking_query, industry_name)
        records = self.dbcursor.fetchall()
        
        return records

    def retrieve_industry_wise_business(self, industry_name):
        industry_business_records, industry_event_total = [], []
        event_fetch = ('SELECT Id,Name FROM EVENT')
        self.dbcursor.execute(event_fetch)
        event_ids = self.dbcursor.fetchall()

        for event_id in event_ids:
            business_query = ('''SELECT t1.Spend
                            FROM megaconsumercard AS t1
                            JOIN booking AS t2 ON t2.Id = t1.Booking_Id
                            JOIN exhibitor AS t3 ON t3.Id = t2.Exhibitor_Id
                            JOIN industry AS t4 ON  t4.Id = t3.Industry_Id
                            WHERE t4.IndustryName = %(IndustryName)s AND t1.Event_Id = %(Event_Id)s
                            ORDER BY t1.Event_id ASC''')
            
            self.dbcursor.execute(business_query,{'IndustryName': industry_name, 'Event_Id':event_id[0]})
            industry_business_records = self.dbcursor.fetchall()
            total_business = 0
            for record in industry_business_records:
                total_business += record[0]
            industry_event_total.append([event_id[1], total_business])

        return industry_event_total

    def update_record(self, table_name, Id, updated_data):
        set_values = ''

        for i, columns in enumerate(updated_data.keys()):
            if i != len(updated_data.keys())-1:
                set_values += f'{columns} = %({columns})s,'
            else:
                set_values += f'{columns} = %({columns})s WHERE Id = %(Id)s'
        
        updated_data['Id'] = Id
        update_query = (f'UPDATE {table_name} SET '+ set_values)
        print(update_query)
        try:
            self.dbcursor.execute(update_query, updated_data)
            self.connector.commit()
        except Exception as e:
            print(' *** Updation Failed *** \n', e)

    def fetch_column_data(self, table_name, columns, condition_name=None, condition_value=None):
        fetch_query = 'SELECT '
        if columns[0].lower() == 'all':
            columns = ['*']

        for i,column in enumerate(columns):
            if i < len(columns)-1:
                fetch_query += f'{column}, '
            else:
                fetch_query += f'{column} FROM {table_name}'
        
        if condition_name != None and condition_value != None:
            fetch_query += f' WHERE {condition_name} = %(condition_value)s'
            print(fetch_query)
            self.dbcursor.execute(fetch_query, {'condition_value': condition_value})
        else:
            self.dbcursor.execute(fetch_query)
        columns_data = self.dbcursor.fetchall()

        return columns_data

    def get_last_insert_id(self):
        count_query = (f'SELECT last_insert_id()')
        
        self.dbcursor.execute(count_query)
        no_records = self.dbcursor.fetchone()
        return no_records[0]

    def retrieve_allindustry_bookings(self):
        industry_book_data = []

        industry_query = ('SELECT IndustryName FROM Industry')
        self.dbcursor.execute(industry_query)
        industries = self.dbcursor.fetchall()

        for industry in industries:
            records = self.retrieve_industry_bookings({'IndustryName': industry[0]})
            for record in records:
                industry_book_data.append(record)
        
        return industry_book_data


import mysql.connector
from mysql.connector import errorcode

config = {
  'user': 'root',
  'password': '',
  'host': '127.0.0.1',
  'database': '',
  'raise_on_warnings': True
}

config2 = {
  'user': 'root',
  'password': '',
  'host': '127.0.0.1',
  'database': 'HOTEL_RESERVATION',
  'raise_on_warnings': True
}

print("dsdsd")
class DatabaseManagerMYSQLClass():
    def __init__(self):
        super(DatabaseManagerMYSQLClass, self).__init__()
        print("sasasa")
        try:
            self.conn = mysql.connector.connect(**config)
            self.c = self.conn.cursor()
            #print("sdsdsd")

        except mysql.connector.Error as err:
            #print("sasasaasasas")
            print(err)
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

        else:
            createDatabase(self)
            self.conn.close()

def createDatabase(self):
    sql_0 = "CREATE DATABASE IF NOT EXISTS HOTEL_RESERVATION;"
    print(sql_0)

    try:
        self.c.execute(sql_0)
        self.c.commit()
        print("DATABASE created successfully")
    except mysql.connector.Error as err:
        print("Database created failed")
        print(err)
    finally:
        createTable(self)

def createTable(self):

    sql_0 = ("use HOTEL_RESERVATION;")

    sql_1 = ("CREATE TABLE IF NOT EXISTS `hotel_reservation`.`customer` ("
             " `CustomerID` INT NOT NULL AUTO_INCREMENT ,"
             " `FullName` TEXT ,"
             " `PhoneNumber` VARCHAR(11) NOT NULL,"
             " `Address` TEXT ,"
             " `Password` TEXT NOT NULL DEFAULT '' ,"
             " `Status` TEXT ,"
             " `Remarks` TEXT ,"
             " `GuestCount` INT DEFAULT '0' ,"
             " PRIMARY KEY (`CustomerID`),"
             " UNIQUE (`PhoneNumber`)"
             ") ENGINE = InnoDB;")

    sql_2 = ("CREATE TABLE IF NOT EXISTS `hotel_reservation`.`room_info` ("
             " `RoomNo` INT NOT NULL AUTO_INCREMENT ,"
             " `SuiteName` TEXT NOT NULL ,"
             " `Description` TEXT NOT NULL ,"
             " `isActive` BOOLEAN NOT NULL ,"
             " `CustomerID` INT NULL DEFAULT NULL ,"
             " `Remarks` TEXT NULL DEFAULT NULL ,"
             " `Tag` TEXT NOT NULL ,"
             " PRIMARY KEY (`RoomNo`),"
             " FOREIGN KEY (`CustomerID`) REFERENCES customer(`CustomerID`)"
             ") ENGINE = InnoDB;")

    sql_3 = ("CREATE TABLE IF NOT EXISTS `hotel_reservation`.`reservation` ("
             " `ReservationID` INT NOT NULL AUTO_INCREMENT ,"
             " `CustomerID` INT NOT NULL ,"
             " `Check_in_Date` DATE NOT NULL ,"
             " `Check_in_Time` TIME NOT NULL ,"
             " `Check_out_Date` DATE NOT NULL ,"
             " `Check_out_Time` TIME NOT NULL ,"
             " `Singlebed` INT DEFAULT '0' ,"
             " `DoubleBed` INT DEFAULT '0' ,"
             " `Familyroom` INT DEFAULT '0' ,"
             " `Ameni_spa` BOOLEAN DEFAULT '0',"
             " `Ameni_petroom` BOOLEAN DEFAULT '0',"
             " `Ameni_Breakfast` BOOLEAN DEFAULT '0',"
             " `Payment_method` TEXT NOT NULL ,"
             " `Amount` DECIMAL NOT NULL DEFAULT '0' ,"
             " `Balance` DECIMAL NOT NULL DEFAULT '0' ,"
             " `Room_No` INT NOT NULL ,"
             " `Status` TEXT NOT NULL ,"
             " `Remarks` TEXT ,"
             " PRIMARY KEY (`ReservationID`)"
             ") ENGINE = InnoDB;")


    print(sql_0)
    print(sql_1)
    print(sql_2)
    print(sql_3)

    try:
        self.c.execute(sql_0)
        print("Table created successfully")
    except mysql.connector.Error as err:
        print("Table created failed")
        print(err)

    try:
        self.c.execute(sql_1)
        print("Table created successfully")
    except mysql.connector.Error as err:
        print("Table created failed")
        print(err)

    try:
        self.c.execute(sql_2)
        print("Table created successfully")
    except mysql.connector.Error as err:
        print("Table created failed")
        print(err)

    try:
        self.c.execute(sql_3)
        print("Table created successfully")
    except mysql.connector.Error as err:
        print("Table created failed")
        print(err)

    self.conn.close()

def getDataPhoneNumberIfExist(phoneNumber):
    conn = mysql.connector.connect(**config2)
    c = conn.cursor()

    sql = ("SELECT * FROM CUSTOMER WHERE PHONENUMBER = '" + str(phoneNumber) + "';")
    print(sql)
    c.execute(sql)

    items = None
    items = c.fetchone()
    if items == None:
        print("no ITEMS DETECTED")
        return None
    else:
        from AccountDATA import Account
        customer_account = None
        customer_account = Account
        print(items)

        customer_account.customerID = str(items[0])
        customer_account.customerPhoneNumber = items[2]
        customer_account.customerFullName = items[1]
        customer_account.customerAddress = items[3]

        return customer_account

def checkPhoneNumberisRegistered(phoneNumber):
    conn = mysql.connector.connect(**config2)
    c = conn.cursor()

    sql = ("SELECT CUSTOMERID FROM CUSTOMER WHERE PHONENUMBER = '" + phoneNumber + "' AND PASSWORD IS NOT NULL;")
    print(sql)
    c.execute(sql)
    items = None
    items = c.fetchone()
    if items != None:
        print("ITEMS DETECTED")
        print("EXISTING CUSTOMER ID", items)
        return True
    else:
        return False

def registerCustomer(phonenumber, password):
    conn = mysql.connector.connect(**config2)
    c = conn.cursor()

    sql_1 = ("INSERT IGNORE INTO CUSTOMER(PHONENUMBER, PASSWORD) "
             "VALUES('" + phonenumber + "', '" + password + "');")
    print(sql_1)
    c.execute(sql_1)

    sql_2 = ("UPDATE CUSTOMER SET PASSWORD = '" + password + "' WHERE PHONENUMBER = '" + phonenumber + "'")
    print(sql_2)
    c.execute(sql_2)
    conn.commit()

    sql_3 = "SELECT CUSTOMERID FROM CUSTOMER WHERE PHONENUMBER = '" + phonenumber + "';"
    print(sql_3)
    c.execute(sql_3)

    customerID = None
    customerID = c.fetchone()
    print("SELECT CUSTOMER_ID: ", customerID)
    return customerID[0]

def loginCustomer(phoneNumber, password):
    conn = mysql.connector.connect(**config2)
    c = conn.cursor()

    sql = ("SELECT CUSTOMERID FROM CUSTOMER WHERE PHONENUMBER = '" + phoneNumber + "' AND PASSWORD = '" + password + "';")
    print(sql)
    c.execute(sql)
    customerData = None
    customerData = c.fetchone()

    print("SELECT CUSTOMER_ID: ", customerData)
    if customerData != None:
        print("ITEMS DETECTED")
        return customerData[0]
    else:
        return None

def getcustomerDetails(customerID):
    conn = mysql.connector.connect(**config2)
    c = conn.cursor()

    sql = ("SELECT * FROM CUSTOMER WHERE CUSTOMERID = '" + str(customerID) + "';")
    c.execute(sql)

    items = None
    items = c.fetchone()
    if items == None:
        print("no ITEMS DETECTED")
        return None
    else:
        from AccountDATA import Account
        customer_account = None
        customer_account = Account
        print(items)

        customer_account.customerID = str(items[0])
        customer_account.customerPhoneNumber = items[2]
        customer_account.customerFullName = items[1]
        customer_account.customerAddress = items[3]
        customer_account.customerStatus = items[5]
        customer_account.customerRemarks = items[6]
        customer_account.customerGuestCount = items[7]

        return customer_account

def insertCustomerInfo(customerPhoneNumber, customerFullName, customerAddress, status, guestcount):
    conn = mysql.connector.connect(**config2)
    c = conn.cursor()

    try:
        sql_1 = ("INSERT IGNORE INTO CUSTOMER(PHONENUMBER, FULLNAME, ADDRESS, STATUS, GUESTCOUNT) "
                 "VALUES('" + customerPhoneNumber + "', '" + customerFullName + "', '" + customerAddress + "', '" + status + "', '" + str(guestcount) + "');")
        print(sql_1)
        c.execute(sql_1)
    except mysql.connector.Error as err:
        print("sql failed")
        print(err)


    sql_2 = ("UPDATE CUSTOMER SET FULLNAME = '" + customerFullName + "', ADDRESS = '" + customerAddress + "', STATUS = '" + status + "', GUESTCOUNT = " + str(guestcount) + " WHERE PHONENUMBER = '" + customerPhoneNumber + "';")
    print(sql_2)
    c.execute(sql_2)

    conn.commit()
    sql_3 = "SELECT CUSTOMERID FROM CUSTOMER WHERE PHONENUMBER = '" + customerPhoneNumber + "';"
    print(sql_3)
    c.execute(sql_3)

    customerID = None
    customerID = c.fetchone()
    print("SELECT CUSTOMERID: ", customerID)
    return customerID[0]

def insertReservationInfo(customerID, checkin_date, checkin_time, checkout_date, checkout_time, singlebed, doublebed, familyroom, ameni_spa, ameni_petroom, ameni_breakfast, paymentmethod, amount, balance, room_no, status, remarks):
    conn = mysql.connector.connect(**config2)
    c = conn.cursor()

    sql_1 = ("INSERT INTO RESERVATION("
             " CUSTOMERID,"
             " CHECK_IN_DATE,"
             " CHECK_IN_TIME,"
             " CHECK_OUT_DATE,"
             " CHECK_OUT_TIME,"
             " SINGLEBED,"
             " DOUBLEBED,"
             " FAMILYROOM,"
             " AMENI_SPA,"
             " AMENI_PETROOM,"
             " AMENI_BREAKFAST,"
             " PAYMENT_METHOD,"
             " AMOUNT,"
             " BALANCE,"
             " ROOM_NO,"
             " STATUS,"
             " REMARKS"
             ") "
             "VALUES("
             "'" + str(customerID) + "', '"
             + str(checkin_date) + "', '"
             + str(checkin_time) + "', '"
             + str(checkout_date) + "', '"
             + str(checkout_time) + "', '"
             + str(singlebed) + "', '"
             + str(doublebed) + "', '"
             + str(familyroom) + "', '"
             + str(ameni_spa) + "', '"
             + str(ameni_petroom) + "', '"
             + str(ameni_petroom) + "', '"
             + str(paymentmethod) + "', '"
             + str(amount) + "', '"
             + str(balance) + "', '"
             + str(room_no) + "', '"
             + status + "' , '"
             + remarks + "');")


    print(sql_1)
    c.execute(sql_1)
    conn.commit()
    print("insertReservationInfo ID:", c.lastrowid)
    return c.lastrowid

def checkcustomerIDandReservationIfExist(customerID):
    conn = mysql.connector.connect(**config2)
    c = conn.cursor()

    sql_3 = "SELECT * FROM CUSTOMER WHERE CUSTOMERID = '" + str(customerID) + "';"
    print(sql_3)
    c.execute(sql_3)

    customerinfo = None
    customerinfo = c.fetchone()
    print("SELECT all : ", customerinfo)

    if customerinfo != None:
        customername = customerinfo[1]

        sql_3 = ("SELECT * FROM RESERVATION WHERE CUSTOMERID = '" + str(customerID) + "' AND STATUS IN ('Reserved','Active');")
        print(sql_3)
        c.execute(sql_3)

        reservationItem = None
        reservationItem= c.fetchone()
        print("SELECT * FROM RESERVATION: ", reservationItem)
        if reservationItem == None:
            print("no ITEMS DETECTED")
            return None
        else:
            from ReservationDATA import Reservation
            reservation_data = None
            reservation_data = Reservation
            print(reservationItem)

            reservation_data.reservation_id = reservationItem[0]
            reservation_data.customer_id = reservationItem[1]
            reservation_data.customer_name = customername
            reservation_data.checkin_date = reservationItem[2]
            reservation_data.checkout_date = reservationItem[4]
            reservation_data.room_no = reservationItem[15]
            reservation_data.singlebed = reservationItem[6]
            reservation_data.doublebed = reservationItem[7]
            reservation_data.familyroom = reservationItem[8]
            reservation_data.ameni_spa = reservationItem[9]
            reservation_data.ameni_petroom = reservationItem[10]
            reservation_data.ameni_breakfast = reservationItem[11]
            reservation_data.balance = reservationItem[14]
            reservation_data.status = reservationItem[16]
            reservation_data.remarks = reservationItem[17]

            return reservation_data

def checkRoomNoIfAvailable(roomNumber):
    conn = mysql.connector.connect(**config2)
    c = conn.cursor()

    sql_1 = ("SELECT ROOM_NO FROM RESERVATION WHERE ROOM_NO = '" + str(roomNumber) + "' AND STATUS = 'Reserved';")
    print(sql_1)
    c.execute(sql_1)

    room_No = None
    room_No = c.fetchone()
    print("SELECT CUSTOMERID: ", room_No)
    if room_No == None:
        return True
    else: return False

def updateReservationStatus(reservation_ID, status):
    conn = mysql.connector.connect(**config2)
    c = conn.cursor()

    sql_1 = ("UPDATE RESERVATION SET STATUS = '" + status + "' WHERE RESERVATIONID = '" + str(reservation_ID) + "'")
    print(sql_1)
    c.execute(sql_1)
    conn.commit()

def updateCustomerStatus(customer_ID, status, guest):
    conn = mysql.connector.connect(**config2)
    c = conn.cursor()

    sql_1 = ("UPDATE CUSTOMER SET STATUS = '" + status + "', GUESTCOUNT = '" + str(guest) + "'  WHERE CUSTOMERID = '" + str(customer_ID) + "'")
    print(sql_1)
    c.execute(sql_1)
    conn.commit()

def updateReservationBalance(reservation_ID, balance):
    conn = mysql.connector.connect(**config2)
    c = conn.cursor()

    sql_1 = ("UPDATE RESERVATION SET BALANCE = '" + str(balance) + "' WHERE RESERVATIONID = '" + str(reservation_ID) + "'")
    print(sql_1)
    c.execute(sql_1)
    conn.commit()

def getAllReservationData():
    conn = mysql.connector.connect(**config2)
    c = conn.cursor()

    sql = ("SELECT * "
           " FROM RESERVATION"
           " INNER JOIN CUSTOMER on CUSTOMER.CUSTOMERID = RESERVATION.CUSTOMERID;")
    print(sql)
    c.execute(sql)

    items = None
    items = c.fetchall()

    return items

def findCustomersName(name):
    conn = mysql.connector.connect(**config2)
    c = conn.cursor()

    sql = ("SELECT COUNT(CustomerID) FROM customer WHERE FULLNAME LIKE '%"+name+"%';")
    print(sql)
    c.execute(sql)

    count = None
    count = c.fetchone()
    print(count)
    if count[0] > 1:
        return "MULTIPLE"
    elif count[0] == 0:
        return "NO"
    else:
        sql2 = ("SELECT * FROM customer WHERE FULLNAME LIKE '%" + name + "%';")
        print(sql2)
        c.execute(sql2)

        items = None
        items = c.fetchone()
        if items == None:
            print("no ITEMS DETECTED")
            return None
        else:
            from AccountDATA import Account
            customer_account = None
            customer_account = Account
            print(items)

            customer_account.customerID = str(items[0])
            customer_account.customerPhoneNumber = items[2]
            customer_account.customerFullName = items[1]
            customer_account.customerAddress = items[3]
            customer_account.customerStatus = items[5]
            customer_account.customerRemarks = items[6]
            customer_account.customerGuestCount = items[7]

            return customer_account

def findreservationIDandReturnALL(reservationID):
    conn = mysql.connector.connect(**config2)
    c = conn.cursor()

    sql = ("SELECT * "
           " FROM RESERVATION"
           " WHERE RESERVATIONID = '"+ str(reservationID) + "';")
    print(sql)
    c.execute(sql)

    reservationItem = None
    reservationItem = c.fetchone()
    print("SELECT * FROM RESERVATION: ", reservationItem)
    if reservationItem == None:
        print("no ITEMS DETECTED")
        return None
    else:
        from ReservationDATA import Reservation
        reservation_data = None
        reservation_data = Reservation
        print(reservationItem)

        reservation_data.reservation_id = reservationItem[0]
        reservation_data.customer_id = reservationItem[1]
        reservation_data.checkin_date = reservationItem[2]
        reservation_data.checkout_date = reservationItem[4]
        reservation_data.room_no = reservationItem[15]
        reservation_data.singlebed = reservationItem[6]
        reservation_data.doublebed = reservationItem[7]
        reservation_data.familyroom = reservationItem[8]
        reservation_data.ameni_spa = reservationItem[9]
        reservation_data.ameni_petroom = reservationItem[10]
        reservation_data.ameni_breakfast = reservationItem[11]
        reservation_data.balance = reservationItem[14]
        reservation_data.status = reservationItem[16]
        reservation_data.remarks = reservationItem[17]

        return reservation_data


#start class
#database = DatabaseManagerMYSQLClass()

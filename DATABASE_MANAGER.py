import sqlite3
import sys
from PyQt5.QtWidgets import QApplication

class DatabaseManagerClass():
    def __init__(self):
        super(DatabaseManagerClass, self).__init__()

        self.conn = sqlite3.connect('hotel_reservation_database.db')
        self.c = self.conn.cursor()
        createTable(self)

def createTable(self):

    sql_1 = ("CREATE TABLE IF NOT EXISTS 'CUSTOMER'("
    "PK_CUSTOMER_ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, "
    "PHONENUMBER TEXT NOT NULL UNIQUE, "
    "FULLNAME TEXT, "
    "ADDRESS TEXT, "
    "PASSWORD TEXT );")

    sql_2 = ("CREATE TABLE IF NOT EXISTS 'RESERVATION'("
      "PK_RESERVATION_ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, "
      "FK_CUSTOMER_ID INTEGER NOT NULL, "
      "CHECKIN_DATE TEXT NOT NULL, "
      "CHECKIN_TIME TEXT NOT NULL, "
      "CHECKOUT_DATE TEXT NOT NULL, "
      "CHECKOUT_TIME TIME TEXT NOT NULL, "  # full address {lothouse,barangay,citymuni,provice,zipcode}
      "SINGLEBED INTEGER DEFAULT 0, "
      "DOUBLEBED INTEGER DEFAULT 0, " 
      "FAMILYROOM INTEGER DEFAULT 0, "
      "AMENI_SPA TEXT, "
      "AMENI_POOL TEXT, "
      "PAYMENT_METHOD TEXT NOT NULL, "
      "AMOUNT INTEGER NOT NULL, "
      "ROOM_NO INTEGER NOT NULL, "
      "STATUS TEXT,"
      "FOREIGN KEY (FK_CUSTOMER_ID)"
      "REFERENCES CUSTOMER (PK_CUSTOMER_ID)"
             "ON UPDATE CASCADE "
             "ON DELETE CASCADE "
    ");")

    print(sql_1)
    print(sql_2)
    try:
        self.conn.execute(sql_1)
        self.conn.execute(sql_2)
        self.conn.commit()
        print("Table created successfully")
    except :
        print("Table creation error")

    self.conn.close()

def getDataPhoneNumberIfExist(phoneNumber):
    conn = sqlite3.connect('hotel_reservation_database.db')
    c = conn.cursor()

    sql = ("SELECT * FROM CUSTOMER WHERE PHONENUMBER = '" + phoneNumber + "';")
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
        customer_account.customerPhoneNumber = items[1]
        customer_account.customerFullName = items[2]
        customer_account.customerAddress = items[3]

        return customer_account

def insertCustomerInfo(customerPhoneNumber, customerFullName, customerAddress):
    conn = sqlite3.connect('hotel_reservation_database.db')
    c = conn.cursor()

    sql_1 = ("INSERT OR IGNORE INTO CUSTOMER(PHONENUMBER, FULLNAME, ADDRESS) "
             "VALUES('" + customerPhoneNumber + "', '" + customerFullName + "', '" + customerAddress  + "');")
    print(sql_1)
    c.execute(sql_1)
    sql_2 = ("UPDATE CUSTOMER SET FULLNAME = '" + customerFullName + "', ADDRESS = '" + customerAddress + "' WHERE PHONENUMBER = '" + customerPhoneNumber + "'")
    print(sql_2)
    c.execute(sql_2)

    conn.commit()
    sql_3 = "SELECT PK_CUSTOMER_ID FROM CUSTOMER WHERE PHONENUMBER = '" + customerPhoneNumber + "';"
    print(sql_3)
    c.execute(sql_3)

    customerID = None
    customerID = c.fetchone()
    print("SELECT PK_CUSTOMER_ID: ", customerID)
    return customerID[0]

def insertReservationInfo(customerID, checkin_date, checkin_time, checkout_date, checkout_time, singlebed, doublebed, familyroom, spa, pool, paymentmethod, amount, room_no, status):
    conn = sqlite3.connect('hotel_reservation_database.db')
    c = conn.cursor()

    sql_1 = ("INSERT INTO RESERVATION(FK_CUSTOMER_ID, CHECKIN_DATE, CHECKIN_TIME, CHECKOUT_DATE, CHECKOUT_TIME, SINGLEBED, DOUBLEBED, FAMILYROOM, AMENI_SPA, AMENI_POOL, PAYMENT_METHOD, AMOUNT, ROOM_NO, STATUS) "
                        "VALUES('" + str(customerID) + "', '" + str(checkin_date) + "', '" + str(checkin_time) + "', '" + str(checkout_date) + "', '" + str(checkout_time) + "', '" + str(singlebed) + "', '" + str(doublebed) + "', '" + str(familyroom) + "', '" + str(spa) + "', '" + str(pool) + "', '" + str(paymentmethod) + "', '" + str(amount) + "', '" + str(room_no) + "', '" + status + "');")
    print(sql_1)
    c.execute(sql_1)
    conn.commit()
    print("insertReservationInfo ID:", c.lastrowid)
    return c.lastrowid

def checkRoomNoIfAvailable(roomNumber):
    conn = sqlite3.connect('hotel_reservation_database.db')
    c = conn.cursor()

    sql_1 = ("SELECT ROOM_NO FROM RESERVATION WHERE ROOM_NO = '" + str(roomNumber) + "' AND STATUS = 'Reserved';")
    print(sql_1)
    c.execute(sql_1)

    room_No = None
    room_No = c.fetchone()
    print("SELECT PK_CUSTOMER_ID: ", room_No)
    if room_No == None:
        return True
    else: return False

def checkcustomerIDandReservationIfExist(customerID):
    conn = sqlite3.connect('hotel_reservation_database.db')
    c = conn.cursor()

    sql_3 = "SELECT * FROM CUSTOMER WHERE PK_CUSTOMER_ID = '" + str(customerID) + "';"
    print(sql_3)
    c.execute(sql_3)

    customerinfo = None
    customerinfo = c.fetchone()
    print("SELECT all : ", customerinfo)

    if customerinfo != None:
        customername = customerinfo[2]

        sql_3 = ("SELECT * FROM RESERVATION WHERE FK_CUSTOMER_ID = '" + str(customerID) + "' AND STATUS = 'Reserved';")
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
            reservation_data.room_no = reservationItem[13]

            return reservation_data

def updateReservationStatus(reservation_ID, status):
    conn = sqlite3.connect('hotel_reservation_database.db')
    c = conn.cursor()

    sql_1 = ("UPDATE RESERVATION SET STATUS = '" + status + "' WHERE PK_RESERVATION_ID = '" + str(reservation_ID) + "'")
    print(sql_1)
    c.execute(sql_1)
    conn.commit()

def registerCustomer(phonenumber, password):
    conn = sqlite3.connect('hotel_reservation_database.db')
    c = conn.cursor()

    sql_1 = ("INSERT OR IGNORE INTO CUSTOMER(PHONENUMBER, PASSWORD) "
             "VALUES('" + phonenumber + "', '" + password + "');")
    print(sql_1)
    c.execute(sql_1)
    sql_2 = (
                "UPDATE CUSTOMER SET PASSWORD = '" + password + "' WHERE PHONENUMBER = '" + phonenumber + "'")
    print(sql_2)
    c.execute(sql_2)
    conn.commit()

    sql_3 = "SELECT PK_CUSTOMER_ID FROM CUSTOMER WHERE PHONENUMBER = '" + phonenumber + "';"
    print(sql_3)
    c.execute(sql_3)

    customerID = None
    customerID = c.fetchone()
    print("SELECT PK_CUSTOMER_ID: ", customerID)
    return customerID[0]

def checkPhoneNumberisRegistered(phoneNumber):
    conn = sqlite3.connect('hotel_reservation_database.db')
    c = conn.cursor()

    sql = ("SELECT PK_CUSTOMER_ID FROM CUSTOMER WHERE PHONENUMBER = '" + phoneNumber + "' AND PASSWORD IS NOT NULL;")
    c.execute(sql)
    items = None
    items = c.fetchone()
    if items != None:
        print("ITEMS DETECTED")
        print("EXISTING CUSTOMER ID", items)
        return True
    else:
        return False

def loginCustomer(phoneNumber, password):
    conn = sqlite3.connect('hotel_reservation_database.db')
    c = conn.cursor()

    sql = ("SELECT PK_CUSTOMER_ID FROM CUSTOMER WHERE PHONENUMBER = '" + phoneNumber + "' AND PASSWORD = '" + password + "';")
    c.execute(sql)
    customerData = None
    customerData = c.fetchone()

    print("SELECT PK_CUSTOMER_ID: ", customerData)
    if customerData != None:
        print("ITEMS DETECTED")
        return customerData[0]
    else:
        return None

def getcustomerDetails(customerID):
    conn = sqlite3.connect('hotel_reservation_database.db')
    c = conn.cursor()

    sql = ("SELECT * FROM CUSTOMER WHERE PK_CUSTOMER_ID = '" + str(customerID) + "';")
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
        customer_account.customerPhoneNumber = items[1]
        customer_account.customerFullName = items[2]
        customer_account.customerAddress = items[3]

        return customer_account

def getAllReservationData():
    conn = sqlite3.connect('hotel_reservation_database.db')
    c = conn.cursor()

    sql = ("SELECT * "
           " FROM RESERVATION"
           " INNER JOIN CUSTOMER on CUSTOMER.PK_CUSTOMER_ID = RESERVATION.FK_CUSTOMER_ID;")
    c.execute(sql)

    items = None
    items = c.fetchall()


    return items


"""
app = QApplication(sys.argv)
database = DatabaseManagerClass()
app.exec_()
"""

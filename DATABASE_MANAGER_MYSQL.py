import mysql.connector
from mysql.connector import errorcode

config = {
  'user': 'root',
  'password': '',
  'host': '127.0.0.1',
  'database': '',
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
             " `FullName` TEXT NOT NULL DEFAULT '' ,"
             " `PhoneNumber` INT(11) NOT NULL,"
             " `Address` TEXT NOT NULL ,"
             " `Password` TEXT NOT NULL DEFAULT '' ,"
             " `Status` TEXT NOT NULL , `Remarks` TEXT ,"
             " `GuestCount` INT DEFAULT '0' ,"
             " PRIMARY KEY (`CustomerID`),"
             " UNIQUE (`PhoneNumber`)"
             ") ENGINE = InnoDB;")

    sql_2 = ("CREATE TABLE `hotel_reservation`.`room_info` ("
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
             " `Checkout_Date` DATE NOT NULL ,"
             " `Checkout_Time` TIME NOT NULL ,"
             " `Singlebed` INT DEFAULT '0' ,"
             " `DoubleBed` INT DEFAULT '0' ,"
             " `Familyroom` INT DEFAULT '0' ,"
             " `Ameni_spa` BOOLEAN ,"
             " `Ameni_petroom` BOOLEAN ,"
             " `Ameni_Breakfast` BOOLEAN ,"
             " `Payment_method` INT NOT NULL ,"
             " `Amount` DECIMAL NOT NULL DEFAULT '0' ,"
             " `Balance` DECIMAL NOT NULL ,"
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


#start class
database = DatabaseManagerMYSQLClass()

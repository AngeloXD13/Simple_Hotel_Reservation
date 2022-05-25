import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QDateEdit, QTimeEdit, QRadioButton, QCheckBox, QSpinBox, QTextBrowser
from PyQt5 import uic

from Client_booking_confirmation import ClientBookingConfirmationClass

import random
from PyQt5 import QtCore

from DATABASE_MANAGER_MYSQL import getDataPhoneNumberIfExist
from DATABASE_MANAGER_MYSQL import insertCustomerInfo
from DATABASE_MANAGER_MYSQL import insertReservationInfo
from DATABASE_MANAGER_MYSQL import checkcustomerIDandReservationIfExist


class ClientBookingClass(QMainWindow):
    def __init__(self, windowData):
        super(ClientBookingClass, self).__init__()
        self.windowData = windowData

        uic.loadUi("ui/client_booking.ui", self)

        self.fullname_le = self.findChild(QLineEdit, "fullname_le")
        self.phonenumber_le = self.findChild(QLineEdit, "phonenumber_le")
        self.address_le = self.findChild(QLineEdit, "address_le")

        self.checkin_de = self.findChild(QDateEdit, "checkin_date_de")
        self.checkin_te = self.findChild(QTimeEdit, "checkin_time_te")
        self.checkout_de = self.findChild(QDateEdit, "checkout_date_de")
        self.checkout_te = self.findChild(QTimeEdit, "checkout_time_te")

        self.singlebed_sb = self.findChild(QSpinBox, "singlebed_sb")
        self.doublebed_sb = self.findChild(QSpinBox, "doublebed_sb")
        self.familyroom_sb = self.findChild(QSpinBox, "family_sb")

        self.singlebed_tb = self.findChild(QTextBrowser,"singlebed_tb")
        self.doublebed_tb = self.findChild(QTextBrowser,"doublebed_tb")
        self.familyroom_tb = self.findChild(QTextBrowser,"family_tb")

        self.spa_cb = self.findChild(QCheckBox, "spa_cb")
        self.pool_cb = self.findChild(QCheckBox, "petroom_cb")
        self.breakfast_cb = self.findChild(QCheckBox, "breakfast_cb")

        self.creditcard_rb = self.findChild(QRadioButton, "credit_rb")
        self.paymaya_rb = self.findChild(QRadioButton, "paymaya_rb")
        self.gcash_rb = self.findChild(QRadioButton, "gcash_rb")

        self.amount_tb = self.findChild(QTextBrowser, "totalamount_tb")
        self.status_lbl = self.findChild(QLabel, "status_lbl")
        self.status_lbl.setText("Fill-out Phone number first")
        self.reserve_btn = self.findChild(QPushButton, "reserve_btn")
        self.exit_btn = self.findChild(QPushButton, "exit_btn")


        self.exit_btn.clicked.connect(lambda: gotomenu(self))
        self.reserve_btn.clicked.connect(lambda: insertCustomerDetails(self))

        self.reserve_btn.clicked.connect(lambda: insertCustomerDetails(self))
        self.reserve_btn.setEnabled(False)

        self.reservationIsActive = None
        self.ui = None
        # getActiveValues(self)
        changeSignals(self)
        setCustomerDetails(self)
        self.show()

def setCustomerDetails(self):
    self.phonenumber = self.windowData.accountDATA.customerPhoneNumber
    self.phonenumber_le.setText(self.phonenumber)
    self.phonenumber_le.setReadOnly(True)
    self.phonenumber_le.setDisabled(True)

    checkphonenumber(self)

def changeSignals(self):
    self.checkin_de.dateChanged.connect(lambda: getActiveValues(self))
    self.checkin_te.timeChanged.connect(lambda: getActiveValues(self))
    self.checkout_de.dateChanged.connect(lambda: getActiveValues(self))
    self.checkout_te.timeChanged.connect(lambda: getActiveValues(self))
    self.singlebed_sb.valueChanged.connect(lambda: getActiveValues(self))
    self.doublebed_sb.valueChanged.connect(lambda: getActiveValues(self))
    self.familyroom_sb.valueChanged.connect(lambda: getActiveValues(self))
    self.spa_cb.stateChanged.connect(lambda: getActiveValues(self))
    self.pool_cb.stateChanged.connect(lambda: getActiveValues(self))
    self.creditcard_rb.released.connect(lambda: getActiveValues(self))
    self.paymaya_rb.released.connect(lambda: getActiveValues(self))
    self.gcash_rb.released.connect(lambda: getActiveValues(self))
    self.fullname_le.textChanged.connect(lambda: getActiveValues(self))
    self.address_le.textChanged.connect(lambda: getActiveValues(self))

def refreshAmount(self):
    subtotalamount = 0
    totalSingleBed = int(self.singlebed) * 950
    totalDoubleBed = int(self.doublebed) * 1200
    totalFamilyRoom = int(self.familyroom) * 3600
    amenities = 0
    if self.spa == True:
        amenities = amenities + 500
    if self.pool == True:
        amenities = amenities + 250
    subtotalamount = totalSingleBed + totalDoubleBed + totalFamilyRoom + amenities
    self.totaldays = int(self.checkout_date[2]) - int(self.checkin_date[2])

    self.totalamount = 0
    self.totalamount = subtotalamount * self.totaldays
    # set
    self.singlebed_tb.clear()
    self.doublebed_tb.clear()
    self.familyroom_tb.clear()

    if self.singlebed != 0:
        self.singlebed_tb.setText(str(totalSingleBed))
    if self.doublebed != 0:
        self.doublebed_tb.setText(str(totalDoubleBed))
    if self.familyroom != 0:
        self.familyroom_tb.setText(str(totalFamilyRoom))

    self.amount_tb.setText("₱ {:,.2f}".format(self.totalamount))
    # self.status_lbl
    inputChecker(self)

def inputChecker(self):
    self.status_lbl.clear()
    self.reserve_btn.setEnabled(False)

    if self.phonenumber == '':
        self.status_lbl.setText("Phone Number field is empty")
    elif self.reservationIsActive != None and self.reservationIsActive == True:
        self.status_lbl.setText("Existing Reservation Detected")
        showErrorDialog(self, "Existing Reservation Detected", "Please cancel the previous one before re-booking again...")
    elif int(self.checkout_date[2]) < int(self.checkin_date[2]):
        self.status_lbl.setText("Invalid check-out date")
    elif int(self.singlebed) == 0 and int(self.doublebed) == 0 and int(self.familyroom) == 0:
        self.status_lbl.setText("Add Room")
    elif self.totaldays == 0:
        self.status_lbl.setText("Add days")
    else:
        getPassiveValues(self)
        if self.creditcard == False and self.paymaya == False and self.gcash == False:
            self.status_lbl.setText("Choose Payment Option")
        elif self.fullname == '':
            self.status_lbl.setText("Name field is empty")
        elif self.address == '':
            self.status_lbl.setText("Address field is empty")
        else:
            self.reserve_btn.setEnabled(True)
            self.status_lbl.setText("OK")

def getActiveValues(self):
    print("\n VALUES CHANGE ")
    self.phonenumber = ''
    self.phonenumber = self.phonenumber_le.text()

    self.checkin_date = self.checkin_de.date().getDate()
    self.checkin_date_converted = self.checkin_de.date().toString("yyyy-MM-dd")
    print("self.checkin_date", self.checkin_date)
    print("extracted date", self.checkin_date[2])

    self.checkin_time = self.checkin_te.time().hour()
    print("self.checkin_time", self.checkin_time)

    self.checkout_date = self.checkout_de.date().getDate()
    self.checkout_date_converted = self.checkout_de.date().toString("yyyy-MM-dd")
    print("self.checkout_date", self.checkout_date)

    self.checkout_time = self.checkout_te.time().hour()
    print("self.checkout_time", self.checkout_time)

    self.singlebed = self.singlebed_sb.value()
    print("self.singlebed", self.singlebed)
    self.doublebed = self.doublebed_sb.value()
    print("self.doublebed", self.doublebed)
    self.familyroom = self.familyroom_sb.value()
    print("self.familyroom", self.familyroom)

    self.spa = 0
    if self.spa_cb.isChecked():
        self.spa = 1
        print("self.spa", self.spa)

    self.pool = self.pool_cb.isChecked()
    print("self.pool", self.pool)

    refreshAmount(self)

def getPassiveValues(self):
    self.fullname = ''
    self.address = ''

    self.fullname = self.fullname_le.text()
    self.address = self.address_le.text()

    self.creditcard = self.creditcard_rb.isChecked()
    self.paymaya = self.paymaya_rb.isChecked()
    self.gcash = self.gcash_rb.isChecked()

    self.paymentMethod = None
    if self.creditcard == True:
        self.paymentMethod = "Credit Card"
    elif self.paymaya == True:
        self.paymentMethod = "PayMaya"
    elif self.gcash == True:
        self.paymentMethod = "GCash"

def checkphonenumber(self):
    #self.phonenumber = self.phonenumber_le.text()
    customer_account = getDataPhoneNumberIfExist(self.phonenumber)
    if customer_account != None:
        self.fullname_le.setText(customer_account.customerFullName)
        self.address_le.setText(customer_account.customerAddress)
        self.customer_ID = customer_account.customerID
        reservation_data = checkcustomerIDandReservationIfExist(self.customer_ID)
        self.reservationIsActive = None
        if reservation_data != None:
            self.reservationIsActive = True
            self.status_lbl.setText("Existing Reservation Detected")
            showErrorDialog(self, "Existing Reservation Detected",
                            "Please cancel the previous one before re-booking again...")

def insertCustomerDetails(self):
    getPassiveValues(self)
    customerID = insertCustomerInfo(self.phonenumber, self.fullname, self.address)
    print("insertCustomerDetails_custmerID", customerID)
    insertReservationDetails(self, customerID)

def insertReservationDetails(self, customerID):
    from DATABASE_MANAGER_MYSQL import checkRoomNoIfAvailable
    roomIsAvailable = False
    global tries
    tries = 0
    while roomIsAvailable == False:

        global room_no
        room_no = random.randint(1, 99)
        roomIsAvailable = checkRoomNoIfAvailable(room_no)
        if tries >= 500:
            self.status_lbl.setText("NO ROOM AVAILABLE")
            showErrorDialog(self, "No Room Available at this moment",
                            "Please try again later...")
            break
        tries = tries + 1
    else:
        print(tries)
        if tries != 500:
            print("INSERT RESERVATION")
            reservationID = insertReservationInfo(customerID,
                                  self.checkin_date_converted,
                                  self.checkin_time,
                                  self.checkout_date_converted,
                                  self.checkout_time,
                                  self.singlebed,
                                  self.doublebed,
                                  self.familyroom,
                                  self.spa,
                                 "0", #TODO PETROOM
                                "0", # TODO: breakfast
                                  self.paymentMethod,
                                  self.totalamount,
                                "0", # TODO: balance
                                  room_no,
                                  "Reserved",
                                 "None" # TODO: REMARKS
                                                  )
            self.status_lbl.setText("SUCCESSS")
            self.reserve_btn.setEnabled(False)
            self.reserve_btn.disconnect()

            gotobookingconfirmation(self, customerID, room_no)
            ##get reservation details

def gotomenu(self):

    if self.ui != None:
        self.ui.destroy()

    menu = None
    menu = self.windowData.previousWindow
    self.destroy()
    menu.show()

def gotobookingconfirmation(self, customerID, room_no):
    self.windowData.nextWindow = None
    self.windowData.nextWindow = self
    self.destroy()
    self.ui = ClientBookingConfirmationClass(self.windowData)
    self.ui.roomNumber_lbl.setText(str(room_no))
    self.ui.customerID_lbl.setText(str(customerID))

def showErrorDialog(self, errorText,  errorText2):
    from Client_booking_failed import ClientBookingFailedClass

    self.show()

    self.ui = ClientBookingFailedClass(self.windowData)
    self.ui.scenario_lbl.setText(errorText)
    self.ui.scenario_lbl2.setText(errorText2)

    self.ui.ok_btn.clicked.connect(lambda : gotomenu(self))
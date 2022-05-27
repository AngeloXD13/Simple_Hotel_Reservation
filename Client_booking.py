import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QDateEdit, QTimeEdit, QRadioButton, QCheckBox, QSpinBox, QTextBrowser
from PyQt5 import uic

from Client_booking_confirmation import ClientBookingConfirmationClass
from Client_booking_checkout import ClientBookingCheckoutClass

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
        self.petroom_cb = self.findChild(QCheckBox, "petroom_cb")
        self.breakfast_cb = self.findChild(QCheckBox, "breakfast_cb")

        self.adult_sb = self.findChild(QSpinBox, "adults_sb")
        self.children_sb = self.findChild(QSpinBox, "children_sb")

        self.amount_tb = self.findChild(QTextBrowser, "totalamount_tb")
        self.status_lbl = self.findChild(QLabel, "status_lbl")
        self.status_lbl.setText("Fill-out Phone number first")

        self.checkout_btn = self.findChild(QPushButton, "checkout_btn")

        self.remarks_le = self.findChild(QLineEdit, "remarks_le")

        self.exit_btn = self.findChild(QPushButton, "exit_btn")
        self.exit_btn.clicked.connect(lambda: gotomenu(self))

        self.checkout_btn.clicked.connect(lambda: gotocheckout(self))
        self.checkout_btn.setEnabled(False)

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
    self.petroom_cb.stateChanged.connect(lambda: getActiveValues(self))
    self.breakfast_cb.stateChanged.connect(lambda: getActiveValues(self))

    self.fullname_le.textChanged.connect(lambda: getActiveValues(self))
    self.address_le.textChanged.connect(lambda: getActiveValues(self))

    self.adult_sb.valueChanged.connect(lambda: getActiveValues(self))
    self.children_sb.valueChanged.connect(lambda: getActiveValues(self))

def refreshAmount(self):
    subtotalamount = 0
    totalSingleBed = int(self.singlebed) * 950
    totalDoubleBed = int(self.doublebed) * 1200
    totalFamilyRoom = int(self.familyroom) * 3600
    amenities = 0
    if self.spa == 1 :
        amenities = amenities + 500
    if self.petroom == 1 :
        amenities = amenities + 250
    if self.breakfast == 1:
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
    self.checkout_btn.setEnabled(False)

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
        if self.fullname == '':
            self.status_lbl.setText("Name field is empty")
        elif self.address == '':
            self.status_lbl.setText("Address field is empty")
        elif self.guestCount == 0:
            self.status_lbl.setText("Add guests")
        else:
            self.checkout_btn.setEnabled(True)
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

    self.petroom = 0
    if self.petroom_cb.isChecked():
        self.petroom = 1
        print("self.petroom", self.petroom)

    self.breakfast = 0
    if self.breakfast_cb.isChecked():
        self.breakfast = 1
        print("self.breakfast", self.breakfast)

    refreshAmount(self)

def getPassiveValues(self):
    self.fullname = ''
    self.address = ''
    self.remarks = ''
    self.adult = 0
    self.children = 0
    self.guestCount = 0

    self.remarks = self.remarks_le.text()
    self.fullname = self.fullname_le.text()
    self.address = self.address_le.text()

    self.adult = self.adult_sb.value()
    self.children = self.children_sb.value()
    self.guestCount = self.adult + self.children


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
    customerID = insertCustomerInfo(self.phonenumber, self.fullname, self.address, "Reserved", self.guestCount)
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
                                  self.petroom,
                                  self.breakfast,
                                  self.ui.paymentMethod,
                                  self.totalamount,
                                  self.balance,
                                  room_no,
                                  "Reserved",
                                  self.remarks
                                                  )
            self.status_lbl.setText("SUCCESSS")
            self.ui.reserve_btn.setEnabled(False)
            self.ui.reserve_btn.disconnect()
            self.ui.hide()

            self.checkout_btn.setEnabled(False)

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

def gotocheckout(self):

    self.ui = ClientBookingCheckoutClass(self.windowData)

    self.ui.reserve_btn.clicked.connect(lambda: insertCustomerDetails(self))
    self.ui.reserve_btn.setEnabled(False)

    self.ui.rate_tb.setText("₱ {:,.2f}".format(self.totalamount))

    self.ui.downpayment_rb.toggled.connect(lambda: calculatebalance(self))
    self.ui.fullypaid_rb.toggled.connect(lambda: calculatebalance(self))

def calculatebalance(self):

    print("calculate balance")

    self.isdownpayment = 0
    if self.ui.downpayment_rb.isChecked():
        self.isdownpayment = 1

    self.balance = 0
    self.downpayment = 0

    if self.isdownpayment == 1:
        self.downpayment = self.totalamount * 0.20
        self.ui.totalamount_tb.setText("₱ {:,.2f}".format(self.downpayment))
        self.balance = self.totalamount - self.downpayment
    else:
        self.ui.totalamount_tb.setText("₱ {:,.2f}".format(self.totalamount))
        self.balance = 0
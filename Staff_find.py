import random
import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QDateEdit, QTimeEdit, QRadioButton, QCheckBox, QSpinBox, QTextBrowser, QComboBox, QTextEdit
from PyQt5 import uic

from DATABASE_MANAGER_MYSQL import getcustomerDetails
from DATABASE_MANAGER_MYSQL import checkcustomerIDandReservationIfExist
from DATABASE_MANAGER_MYSQL import updateReservationBalance
from DATABASE_MANAGER_MYSQL import updateCustomerStatus
from DATABASE_MANAGER_MYSQL import updateReservationStatus
from DATABASE_MANAGER_MYSQL import getDataPhoneNumberIfExist
from DATABASE_MANAGER_MYSQL import findCustomersName
from DATABASE_MANAGER_MYSQL import findreservationIDandReturnALL

class StaffFindClass(QMainWindow):
    def __init__(self, windowData):
        super(StaffFindClass, self).__init__()
        self.windowData = windowData

        uic.loadUi("ui/staff_find.ui", self)
        self.show()

        self.in_customerID_le = self.findChild(QLineEdit, "in_customerID_le")
        self.in_name_le = self.findChild(QLineEdit, "in_name_le")
        self.in_phonenumber_le = self.findChild(QLineEdit, "in_phonenumber_le")
        self.in_reservationid_le = self.findChild(QLineEdit, "in_reservationid_le")

        self.out_name_le = self.findChild(QLineEdit, "out_name_le")
        self.out_phonenumber_le = self.findChild(QLineEdit, "out_phonenumber_le")
        self.out_address_le = self.findChild(QLineEdit, "out_address_le")
        self.out_status_cb = self.findChild(QComboBox, "out_status_cb")
        self.out_remarks_te = self.findChild(QTextEdit, "out_remarks_te")
        self.out_guest_sb = self.findChild(QSpinBox, "out_guest_sb")

        self.out_checkin_de = self.findChild(QDateEdit, "out_checkin_de")
        self.out_checkout_de = self.findChild(QDateEdit, "out_checkout_de")
        self.roomno_le = self.findChild(QLineEdit, "roomno_le")
        self.out_singlebed_sb = self.findChild(QSpinBox, "out_singlebed_sb")
        self.out_doublebed_sb = self.findChild(QSpinBox, "out_doublebed_sb")
        self.out_familybed_sb = self.findChild(QSpinBox, "out_familybed_sb")
        self.out_spa_cb = self.findChild(QCheckBox, "out_spa_cb")
        self.out_petroom_cb = self.findChild(QCheckBox, "out_petroom_cb")
        self.out_breakfast_cb = self.findChild(QCheckBox, "out_breakfast_cb")
        self.out_rev_remarks_te = self.findChild(QTextEdit, "out_rev_remarks_te")

        self.out_totalamount_tb = self.findChild(QTextBrowser, "out_totalamount_tb")

        self.checkin_pb = self.findChild(QPushButton, "checkin_pb")
        self.checkout_pb = self.findChild(QPushButton, "checkout_pb")
        self.clearbalance_pb = self.findChild(QPushButton, "clearbalance_pb")
        self.exit_btn = self.findChild(QPushButton, "exit_btn")
        self.customerID_btn = self.findChild(QPushButton, "customerID_btn")
        self.name_btn = self.findChild(QPushButton, "name_btn")
        self.phonenumber_btn = self.findChild(QPushButton, "phonenumber_btn")
        self.reservationID_btn = self.findChild(QPushButton, "reservationID_btn")
        self.clear_btn = self.findChild(QPushButton, "clear_btn")

        self.status_lbl = self.findChild(QLabel, "status_lbl")
        self.reservestatus_lbl = self.findChild(QLabel, "reservestatus_lbl")

        self.customerID_btn.clicked.connect(lambda: findcustomerID(self))
        self.phonenumber_btn.clicked.connect(lambda: findphonenumber(self))

        self.checkin_pb.setEnabled(False)
        self.checkout_pb.setEnabled(False)

        self.clear_btn.clicked.connect(lambda : clearForm(self))
        self.exit_btn.clicked.connect(lambda : gotomenu(self))
        self.clearbalance_pb.clicked.connect(lambda : clearbalancenow(self))
        self.checkin_pb.clicked.connect(lambda : checkinnow(self))
        self.checkout_pb.clicked.connect(lambda: checkoutnow(self))
        self.in_name_le.textChanged.connect(lambda: findname(self))
        self.reservationID_btn.clicked.connect(lambda: findreservationID(self))

        setAllReadOnly(self)

def setAllReadOnly(self):
    self.out_name_le.setReadOnly(True)
    self.out_phonenumber_le.setReadOnly(True)
    self.out_address_le.setReadOnly(True)
    self.out_status_cb.setEnabled(False)
    self.out_remarks_te.setReadOnly(True)
    self.out_guest_sb.setReadOnly(True)

    self.out_checkin_de.setReadOnly(True)
    self.out_checkout_de.setReadOnly(True)
    self.roomno_le.setReadOnly(True)
    self.out_singlebed_sb.setReadOnly(True)
    self.out_doublebed_sb.setReadOnly(True)
    self.out_familybed_sb.setReadOnly(True)
    self.out_spa_cb.setCheckable(False)
    self.out_petroom_cb.setCheckable(False)
    self.out_breakfast_cb.setCheckable(False)
    self.out_rev_remarks_te.setReadOnly(True)
    self.out_totalamount_tb.setReadOnly(True)


def findname(self):
    print("findname")
    self.name_btn.setEnabled(False)
    name = self.in_name_le.text()
    if name == "":
        self.status_lbl.setText("Enter Customer Name")
    else:
        customer_account = findCustomersName(name)
        self.status_lbl.setText("")
        if customer_account == None:
            self.status_lbl.setText("Invalid Customer Name")
        elif customer_account == "MULTIPLE":
            self.status_lbl.setText("Multiple Customer found")
        elif customer_account == "NO":
            self.status_lbl.setText("No Customer found")
        else:
            self.name_btn.setEnabled(True)
            self.status_lbl.setText("Customer ID found")
            self.name_btn.clicked.connect(lambda: getCustomerAllDetails(self, customer_account.customerID, 1))


def findphonenumber(self):
    phoneNumber = self.in_phonenumber_le.text()
    customer_account = getDataPhoneNumberIfExist(phoneNumber)
    if customer_account == None:
        self.status_lbl.setText("Invalid Phone Number")
    else:
        self.status_lbl.setText("Customer ID found")
        getCustomerAllDetails(self, customer_account.customerID, 1)


def findreservationID(self):
    reservationID = self.in_reservationid_le.text()
    reservation_data = findreservationIDandReturnALL(reservationID)
    if reservation_data == None:
        self.status_lbl.setText("Invalid Reservation ID")
    else:
        self.status_lbl.setText("Reservation ID found")
        checkifReservationExist(self, reservationID, 2)


def findcustomerID(self):

    customerID = self.in_customerID_le.text()
    customer_account = getcustomerDetails(customerID)
    if customer_account == None:
        self.status_lbl.setText("Invalid Customer ID")
    else:
        self.status_lbl.setText("Customer ID found")
        getCustomerAllDetails(self, customerID, 1)

def getCustomerAllDetails(self, customerID, request):
    # REQUEST FOR RESERVATION ID 1 if active and reserved only. 2 if all
    self.customerID_btn.setEnabled(False)
    self.name_btn.setEnabled(False)
    self.phonenumber_btn.setEnabled(False)
    self.reservationID_btn.setEnabled(False)

    self.reservationID = None

    self.customer_account = None
    self.customer_account = getcustomerDetails(customerID)
    self.out_name_le.setText(self.customer_account.customerFullName)
    self.out_phonenumber_le.setText(self.customer_account.customerPhoneNumber)
    self.out_address_le.setText(self.customer_account.customerAddress)

    # 1 reserved / 2 Active / 3 Inactive / 4 unknown
    if self.customer_account.customerStatus == "Reserved":
        self.out_status_cb.setCurrentIndex(1)
    elif self.customer_account.customerStatus == "Active":
        self.out_status_cb.setCurrentIndex(2)
    elif self.customer_account.customerStatus == "Inactive":
        self.out_status_cb.setCurrentIndex(3)
    else:
        self.out_status_cb.setCurrentIndex(4)

    self.out_remarks_te.setText(self.customer_account.customerRemarks)
    self.out_guest_sb.setValue(self.customer_account.customerGuestCount)

    if request == 1:
        checkifReservationExist(self, customerID, 1)

def checkifReservationExist(self, reference, request):
    #REQUEST 1 if active and reserved only. 2 if all
    self.reservation_data = None
    if request == 1 :
        self.reservation_data = checkcustomerIDandReservationIfExist(reference)
    elif request == 2 :
        self.reservation_data = findreservationIDandReturnALL(reference)
        if self.reservation_data != None:
            getCustomerAllDetails(self, self.reservation_data.customer_id, 2)


    if self.reservation_data == None:
        self.status_lbl.setText("Customer ID found but no Active Reservations")
        self.reservestatus_lbl.setText("No reservation found")
        self.checkout_pb.setEnabled(False)
        self.checkin_pb.setEnabled(False)
        self.clearbalance_pb.setEnabled(False)
    else:
        self.out_checkin_de.setDate(self.reservation_data.checkin_date)
        self.out_checkout_de.setDate(self.reservation_data.checkout_date)
        self.out_singlebed_sb.setValue(self.reservation_data.singlebed)
        self.out_doublebed_sb.setValue(self.reservation_data.doublebed)
        self.out_familybed_sb.setValue(self.reservation_data.familyroom)
        if self.reservation_data.ameni_spa == 1:
            self.out_spa_cb.setCheckState(True)
        if self.reservation_data.ameni_petroom == 1:
            self.out_petroom_cb.setCheckState(True)
        if self.reservation_data.ameni_breakfast == 1:
            self.out_breakfast_cb.setCheckState(True)
        self.out_rev_remarks_te.setText(self.reservation_data.remarks)
        self.roomno_le.setText(str(self.reservation_data.room_no))
        self.out_totalamount_tb.setText("₱ {:,.2f}".format(self.reservation_data.balance))

        if self.reservation_data.status == "Reserved":
            self.reservestatus_lbl.setText("Reserved")
            self.checkin_pb.setEnabled(True)
        elif self.reservation_data.status == "Active":
            self.checkin_pb.setEnabled(False)
            self.reservestatus_lbl.setText("Customer On House")
        elif self.reservation_data.status == "Cancelled":
            self.checkin_pb.setEnabled(False)
            self.checkout_pb.setEnabled(False)
            self.reservestatus_lbl.setText("Reservation Cancelled")
        elif self.reservation_data.status == "Completed":
            self.checkin_pb.setEnabled(False)
            self.checkout_pb.setEnabled(False)
            self.reservestatus_lbl.setText("Reservation Completed")
        else:
            self.reservestatus_lbl.setText("Reservation found")

        if self.reservation_data.balance != 0:
            self.checkout_pb.setEnabled(False)
            self.clearbalance_pb.setEnabled(True)
        else:
            self.clearbalance_pb.setEnabled(False)
            if self.reservation_data.status == "Reserved" or self.reservation_data.status == "Cancelled" or self.reservation_data.status == "Completed":
                self.checkout_pb.setEnabled(False)
            else:
                self.checkout_pb.setEnabled(True)



def clearbalancenow(self):
    updateReservationBalance(self.reservation_data.reservation_id, 0)
    self.reservation_data.balance = 0
    self.out_totalamount_tb.setText("₱ {:,.2f}".format(self.reservation_data.balance))
    if self.reservation_data.status == "Reserved":
        self.checkout_pb.setEnabled(False)
    else:
        self.checkout_pb.setEnabled(True)

def checkoutnow(self):
    updateReservationStatus(self.reservation_data.reservation_id, "Completed")
    updateCustomerStatus(self.customer_account.customerID, "Inactive" , 0)
    self.status_lbl.setText("Check-out success")
    self.reservestatus_lbl.setText("Completed")
    self.out_status_cb.setCurrentIndex(3)
    self.checkin_pb.setEnabled(False)
    self.checkout_pb.setEnabled(False)
    self.out_guest_sb.setValue(0)

def checkinnow(self):
    updateReservationStatus(self.reservation_data.reservation_id, "Active")
    updateCustomerStatus(self.customer_account.customerID, "Active" , self.customer_account.customerGuestCount)
    self.status_lbl.setText("Check-in success")
    self.reservestatus_lbl.setText("Active/Check in")
    self.out_status_cb.setCurrentIndex(2)
    self.checkin_pb.setEnabled(False)
    self.checkout_pb.setEnabled(True)

def clearForm(self):
    self.ui = StaffFindClass(self.windowData)
    self.destroy()

def gotomenu(self):
    menu = self.windowData.previousWindow
    self.destroy()
    menu.show()
import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit
from PyQt5 import uic

from DATABASE_MANAGER_MYSQL import checkcustomerIDandReservationIfExist
from DATABASE_MANAGER_MYSQL import updateReservationStatus
from DATABASE_MANAGER_MYSQL import updateCustomerStatus

from Staff_cancellation_confirm import StaffCancellationConfirmationClass
class StaffCancellationClass(QMainWindow):
    def __init__(self, windowData):
        super(StaffCancellationClass, self).__init__()
        self.windowData = windowData

        uic.loadUi("ui/staff_cancellation.ui", self)

        self.confirm_btn = self.findChild(QPushButton, "confirm_btn")
        self.cancel_btn = self.findChild(QPushButton, "cancel_btn")
        self.customerID_le = self.findChild(QLineEdit, "customernumber_le")
        self.status_lbl = self.findChild(QLabel, "status_lbl")
        self.cancel_btn.clicked.connect(lambda : gotomenu(self))
        self.confirm_btn.setEnabled(False)
        self.customerID_le.textChanged.connect(lambda :checkcustomerID(self))
        self.status_lbl.setText("Fill customer ID")
        self.show()

def checkcustomerID(self):
    self.status_lbl.setText("Fill customer ID")
    self.customerID = None
    self.customerID = self.customerID_le.text()

    if self.customerID != '':
        self.reservation_data = checkcustomerIDandReservationIfExist(self.customerID)
        if self.reservation_data != None:
            self.status_lbl.setText("Customer ID/Reservation found....")
            self.confirm_btn.setEnabled(True)
            self.confirm_btn.clicked.connect(lambda: gotoConfirmation(self))
        elif self.reservation_data == None:
            self.status_lbl.setText("No Customer ID/Reservation found!")
            self.confirm_btn.setEnabled(False)

def gotoConfirmation(self):
    self.hide()
    self.windowData.nextWindow = None
    self.windowData.nextWindow = self

    self.ui = None
    self.ui = StaffCancellationConfirmationClass(self.windowData)
    self.ui.customerID_lbl.setText(self.reservation_data.customer_name + " on " + str(self.reservation_data.checkin_date) + " to " + str(self.reservation_data.checkout_date))

    self.ui.cancel_btn.clicked.connect(lambda: reshowthis(self))
    self.ui.confirm_btn.clicked.connect(lambda: updateDatabase(self))

def reshowthis(self):
    self.ui.destroy()
    self.windowData.nextWindow.show()

def updateDatabase(self):
    updateReservationStatus(self.reservation_data.reservation_id, "Cancelled")
    updateCustomerStatus(self.customerID, "Inactive", 0)
    gotomenu(self)

def gotomenu(self):
    menu = self.windowData.previousWindow
    try:
        self.ui.destroy()
    except:
        pass
    self.destroy()
    menu.show()

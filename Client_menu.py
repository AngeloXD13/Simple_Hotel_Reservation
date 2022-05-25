import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5 import uic

from Client_booking import ClientBookingClass
from Client_cancellation import ClientCancellationClass

from DATABASE_MANAGER_MYSQL import getcustomerDetails
class ClientMenuClass(QMainWindow):
    def __init__(self, windowData):
        super(ClientMenuClass, self).__init__()
        self.windowData = windowData


        uic.loadUi("ui/menu.ui", self)

        self.booking_btn = self.findChild(QPushButton, "booking_btn")
        self.cancelation_btn = self.findChild(QPushButton, "cancelation_btn")
        self.viewReservation_btn = self.findChild(QPushButton, "viewreservation_btn")
        self.logout_btn = self.findChild(QPushButton, "logout_btn")

        self.booking_btn.clicked.connect(lambda: gotobooking(self))
        self.cancelation_btn.clicked.connect(lambda: gotocancelation(self))
        self.viewReservation_btn.clicked.connect(lambda: gotoreservation(self))
        self.logout_btn.clicked.connect(lambda: gotoselection(self))

        getandsetCustomerData(self)
        self.show()


def getandsetCustomerData(self):
    customerID = self.windowData.accountDATA.customerID
    print(customerID)
    account_data = getcustomerDetails(customerID)
    print("account_data", account_data)
    self.windowData.accountDATA = account_data

def gotobooking(self):
    self.windowData.previousWindow = None
    self.windowData.previousWindow = self
    self.hide()
    self.ui = ClientBookingClass(self.windowData)


def gotocancelation(self):
    self.windowData.previousWindow = None
    self.windowData.previousWindow = self
    self.hide()
    self.ui = ClientCancellationClass(self.windowData)


def gotoreservation(self):
    from Client_reservation import ClientViewReservationClass
    self.windowData.previousWindow = None
    self.windowData.previousWindow = self
    self.hide()
    self.ui = ClientViewReservationClass(self.windowData)

def gotoselection(self):
    from Client_selection import ClientSelectionClass
    self.destroy()
    self.ui = ClientSelectionClass()

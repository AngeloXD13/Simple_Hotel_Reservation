import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit
from PyQt5 import uic

from DATABASE_MANAGER_MYSQL import checkcustomerIDandReservationIfExist
from DATABASE_MANAGER_MYSQL import updateReservationStatus
from DATABASE_MANAGER_MYSQL import updateCustomerStatus

class ClientCancellationClass(QMainWindow):
    def __init__(self, windowData):
        super(ClientCancellationClass, self).__init__()
        self.windowData = windowData

        uic.loadUi("ui/client_cancellation.ui", self)

        self.scenario_lbl = self.findChild(QLabel, "scenario_lbl")
        self.yes_btn = self.findChild(QPushButton, "yes_btn")
        self.no_btn = self.findChild(QPushButton, "no_btn")
        self.exit_btn = self.findChild(QPushButton, "exit_btn")

        self.yes_btn.setHidden(True)
        self.no_btn.setHidden(True)
        self.exit_btn.setHidden(True)

        self.customerID = self.windowData.accountDATA.customerID
        checkcustomerID(self)

        self.show()

def checkcustomerID(self):
    self.reservation_data = None
    self.reservation_data = checkcustomerIDandReservationIfExist(self.customerID)
    if self.reservation_data != None:
        if self.reservation_data.status == "Active":
            print("Customer ID/ACTIVE Reservation found....")
            self.scenario_lbl.setText("You have active reservation and not cancelable anymore")
            self.exit_btn.setHidden(False)
            self.exit_btn.clicked.connect(lambda: gotomenu(self))
        else:
            print("Customer ID/RESERVED Reservation found....")
            self.yes_btn.setHidden(False)
            self.no_btn.setHidden(False)
            self.no_btn.clicked.connect(lambda: gotomenu(self))
            self.yes_btn.clicked.connect(lambda: updateDatabase(self))

    elif self.reservation_data == None:
        print("No Customer ID/Reservation found!")
        self.scenario_lbl.setText("You don't have any active and current reservation...")
        self.exit_btn.setHidden(False)
        self.exit_btn.clicked.connect(lambda: gotomenu(self))



def updateDatabase(self):
    updateReservationStatus(self.reservation_data.reservation_id, "Cancelled")
    updateCustomerStatus(self.customerID, "Inactive", 0)
    gotomenu(self)

def gotomenu(self):
    menu = None
    menu = self.windowData.previousWindow
    self.destroy()
    menu.show()

import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit
from PyQt5 import uic

from DATABASE_MANAGER import checkcustomerIDandReservationIfExist
class ClientViewReservationClass(QMainWindow):
    def __init__(self, windowData):
        super(ClientViewReservationClass, self).__init__()
        self.windowData = windowData

        self.customer_ID = self.windowData.accountDATA.customerID
        checkreservation(self)

def checkreservation(self):
    self.reservation_data = None
    self.reservation_data = checkcustomerIDandReservationIfExist(self.customer_ID)
    if self.reservation_data != None:
        print("Reservation Detected")
        setLayoutReservationDetected(self)
    else:
        print("No Reservation Detected")
        setLayoutNoReservationDetected(self)

def setLayoutReservationDetected(self):
    uic.loadUi("ui/client_reservation.ui", self)

    self.ok_btn = self.findChild(QPushButton, "ok_btn")
    self.roomno_lbl = self.findChild(QLabel, "roomnumberid_lbl")
    self.customerId_lbl = self.findChild(QLabel, "customerid_lbl")
    self.checkin_lbl = self.findChild(QLabel, "checkin_lbl")
    self.checkout_lbl = self.findChild(QLabel, "checkout_lbl")

    self.roomno_lbl.setText(str(self.reservation_data.room_no))
    self.customerId_lbl.setText(str(self.customer_ID))
    self.checkin_lbl.setText(str(self.reservation_data.checkin_date))
    self.checkout_lbl.setText(str(self.reservation_data.checkout_date))

    self.ok_btn.clicked.connect(lambda : gotomenu(self))

    self.show()

def setLayoutNoReservationDetected(self):
    uic.loadUi("ui/client_noreservation.ui", self)

    self.customerId_lbl = self.findChild(QLabel, "customerid_lbl")
    self.ok_btn = self.findChild(QPushButton, "ok_btn")

    self.customerId_lbl.setText(str(self.customer_ID))

    self.ok_btn.clicked.connect(lambda: gotomenu(self))

    self.show()

def gotomenu(self):
    menu = None
    menu = self.windowData.previousWindow
    self.destroy()
    menu.show()

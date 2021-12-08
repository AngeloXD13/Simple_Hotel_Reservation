import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QDateEdit, QTimeEdit, QRadioButton, QCheckBox, QSpinBox, QTextBrowser
from PyQt5 import uic


class ClientBookingConfirmationClass(QMainWindow):
    def __init__(self, windowData):
        super(ClientBookingConfirmationClass, self).__init__()
        self.windowData = windowData

        uic.loadUi("ui/client_booking_confirm.ui", self)

        self.roomNumber_lbl = self.findChild(QLabel, "roomnumberid_lbl")
        self.customerID_lbl = self.findChild(QLabel, "customerid_lbl")

        self.ok_btn = self.findChild(QPushButton, "ok_btn")

        self.ok_btn.clicked.connect(lambda : gotomenu(self))

        self.show()

def gotomenu(self):
    menu = None
    menu = self.windowData.previousWindow
    self.destroy()
    menu.show()

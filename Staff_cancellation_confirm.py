import sys
from PyQt5.QtWidgets import QDialog, QPushButton, QLabel, QLineEdit
from PyQt5 import uic


class StaffCancellationConfirmationClass(QDialog):
    def __init__(self, windowData):
        super(StaffCancellationConfirmationClass, self).__init__()
        self.windowData = windowData

        uic.loadUi("ui/staff_cancellation_confirm.ui", self)

        self.customerID_lbl = self.findChild(QLabel, "customername_lbl")
        self.confirm_btn = self.findChild(QPushButton, "confirm_btn")
        self.cancel_btn = self.findChild(QPushButton, "cancel_btn")

        self.show()


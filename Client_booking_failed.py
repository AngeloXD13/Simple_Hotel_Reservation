from PyQt5.QtWidgets import QDialog, QPushButton, QLabel
from PyQt5 import uic

class ClientBookingFailedClass(QDialog):
    def __init__(self, windowData):
        super(ClientBookingFailedClass, self).__init__()
        self.windowData = windowData

        uic.loadUi("ui/client_booking_fail.ui", self)

        self.scenario_lbl = self.findChild(QLabel, "scenario_lbl")
        self.scenario_lbl2 = self.findChild(QLabel, "scenario_lbl_2")
        self.ok_btn = self.findChild(QPushButton, "ok_btn")
        print("client_booking_failed")
        self.show()

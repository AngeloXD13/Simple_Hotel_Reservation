import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5 import uic

from WindowDATA import WindowDatas

from Staff_booking import StaffBookingClass
from Staff_cancellation import StaffCancellationClass
from Staff_reservation import StaffReservationClass
from Staff_find import StaffFindClass

from DATABASE_MANAGER_MYSQL import DatabaseManagerMYSQLClass

class InterfaceStaffClass(QMainWindow):
    def __init__(self):
        super(InterfaceStaffClass, self).__init__()

        self.windowdata = None
        self.windowdata = WindowDatas

        database = DatabaseManagerMYSQLClass()

        uic.loadUi("ui/menu_staff.ui", self)

        self.booking_btn = self.findChild(QPushButton, "booking_btn")
        self.cancelation_btn = self.findChild(QPushButton, "cancelation_btn")
        self.viewReservation_btn = self.findChild(QPushButton, "viewreservation_btn")
        self.findbooking_btn = self.findChild(QPushButton, "findbooking_btn")

        self.logout_btn = self.findChild(QPushButton, "logout_btn")
        self.logout_btn.hide()

        self.booking_btn.clicked.connect(lambda: gotobooking(self))
        self.cancelation_btn.clicked.connect(lambda: gotocancelation(self))
        self.viewReservation_btn.clicked.connect(lambda:gotoreservation(self))
        self.findbooking_btn.clicked.connect(lambda: gotofind(self))

        self.show()

def gotobooking(self):
    self.windowdata.previousWindow = None
    self.windowdata.previousWindow = self
    self.hide()
    self.ui = StaffBookingClass(self.windowdata)

def gotocancelation(self):
    self.windowdata.previousWindow = None
    self.windowdata.previousWindow = self
    self.hide()
    self.ui = StaffCancellationClass(self.windowdata)

def gotoreservation(self):
    self.windowdata.previousWindow = None
    self.windowdata.previousWindow = self
    self.hide()
    self.ui = StaffReservationClass(self.windowdata)

def gotofind(self):
    self.windowdata.previousWindow = None
    self.windowdata.previousWindow = self
    self.hide()
    self.ui = StaffFindClass(self.windowdata)



app = QApplication(sys.argv)
interfaceStaff = InterfaceStaffClass()
app.exec_()

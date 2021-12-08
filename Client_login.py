import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel
from PyQt5 import uic

class ClientLoginClass(QMainWindow):
    def __init__(self, windowData):
        super(ClientLoginClass, self).__init__()
        self.windowData = windowData

        uic.loadUi("ui/client_login.ui", self)

        self.cancel_btn = self.findChild(QPushButton, "cancel_btn")
        self.signin_btn = self.findChild(QPushButton, "signin_btn")
        self.phonenumber_le = self.findChild(QLineEdit, "phonenumber_le")
        self.password_le = self.findChild(QLineEdit, "password_le")
        self.status_lbl = self.findChild(QLabel, "status_lbl")
        self.phonenumber_le.textChanged.connect(lambda: clearstatus(self))
        self.password_le.textChanged.connect(lambda: clearstatus(self))
        self.cancel_btn.clicked.connect(lambda : gotoselection(self))
        self.signin_btn.clicked.connect(lambda : checkvaluesandpassword(self))
        self.show()

def clearstatus(self):
    self.status_lbl.setText("")

def getValues(self):
    self.phonenumber = None
    self.phonenumber = self.phonenumber_le.text()
    self.password = None
    self.password = self.password_le.text()

def checkvaluesandpassword(self):
    self.status_lbl.setText("")
    getValues(self)
    if self.phonenumber == "":
        self.status_lbl.setText("*Enter Phone Number")
    elif self.password == "":
        self.status_lbl.setText("*Enter Password")
    else:
        self.status_lbl.setText("LOADING...")
        checkdatabase(self)

def checkdatabase(self):
    print("checkdatabase")
    from DATABASE_MANAGER import loginCustomer
    from AccountDATA import Account
    self.customerID = None
    self.customerID = loginCustomer(self.phonenumber, self.password)

    if self.customerID == None:
        self.status_lbl.setText("Phone Number and Password does not match")
    else:
        newaccount = None
        newaccount = Account
        newaccount.customerID = self.customerID
        self.windowData.accountDATA = newaccount
        gotomenu(self)

def gotoselection(self):
    selection = self.windowData.previousWindow
    self.destroy()
    selection.show()

def gotomenu(self):
    from Client_menu import ClientMenuClass
    self.destroy()
    self.ui = ClientMenuClass(self.windowData)



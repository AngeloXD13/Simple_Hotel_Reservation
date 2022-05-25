import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel
from PyQt5 import uic

from DATABASE_MANAGER_MYSQL import checkPhoneNumberisRegistered

class ClientRegisterClass(QMainWindow):
    def __init__(self, windowData):
        super(ClientRegisterClass, self).__init__()
        self.windowData = windowData

        uic.loadUi("ui/client_register.ui", self)

        self.cancel_btn = self.findChild(QPushButton, "cancel_btn")
        self.signup_btn = self.findChild(QPushButton, "signup_btn")
        self.phonenumber_le = self.findChild(QLineEdit, "phonenumber_le")
        self.password_le = self.findChild(QLineEdit, "password_le")
        self.password_le2 = self.findChild(QLineEdit, "password_le2")
        self.status_lbl = self.findChild(QLabel, "status_lbl")

        self.cancel_btn.clicked.connect(lambda: gotoselection(self))
        self.signup_btn.clicked.connect(lambda: checkvaluesandpassword(self))
        self.phonenumber_le.editingFinished.connect(lambda: checkifphonenumberregistered(self))


        self.show()

def getValues(self):
    self.phonenumber = self.phonenumber_le.text()
    self.password = None
    self.password2 = None
    self.password = self.password_le.text()
    self.password2 = self.password_le2.text()

def checkvaluesandpassword(self):
    self.status_lbl.setText("")
    getValues(self)
    if self.phonenumber == "":
        self.status_lbl.setText("*Enter Phone Number")
    elif self.password == "" or self.password2 == "":
        self.status_lbl.setText("*Enter Password")
    elif self.password != self.password2:
        self.status_lbl.setText("*Password does not Match")
    else:
        self.status_lbl.setText("LOADING...")
        savetodatabase(self)

def savetodatabase(self):
    print("savetodatabase")
    from DATABASE_MANAGER_MYSQL import registerCustomer
    from AccountDATA import Account
    self.customerID = registerCustomer(self.phonenumber, self.password)

    newaccount = None
    newaccount = Account
    newaccount.customerID = self.customerID
    self.windowData.accountDATA = newaccount
    gotomenu(self)

def checkifphonenumberregistered(self):
    self.signup_btn.setEnabled(True)
    self.phonenumber = self.phonenumber_le.text()
    self.status_lbl.setText("")
    result = None
    result = checkPhoneNumberisRegistered(self.phonenumber)
    if result == True:
        self.status_lbl.setText("This Phone Number have already an account")
        self.signup_btn.setEnabled(False)

def gotoselection(self):
    selection = self.windowData.previousWindow
    self.destroy()
    selection.show()

def gotomenu(self):
    from Client_menu import ClientMenuClass
    self.destroy()
    self.ui = ClientMenuClass(self.windowData)

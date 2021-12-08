import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5 import uic

from WindowDATA import WindowDatas
from Client_login import ClientLoginClass
from Client_register import ClientRegisterClass

class ClientSelectionClass(QMainWindow):
    def __init__(self):
        super(ClientSelectionClass, self).__init__()

        self.windowdata = None
        self.windowdata = WindowDatas

        uic.loadUi("ui/client_loginregister.ui", self)

        self.login_btn = self.findChild(QPushButton, "login_btn")
        self.register_btn = self.findChild(QPushButton, "register_btn")

        self.login_btn.clicked.connect(lambda : gotologin(self))
        self.register_btn.clicked.connect(lambda: gotoregister(self))

        self.show()


def gotologin(self):
    self.windowdata.previousWindow = None
    self.windowdata.previousWindow = self
    self.hide()
    self.ui = ClientLoginClass(self.windowdata)

def gotoregister(self):
    self.windowdata.previousWindow = None
    self.windowdata.previousWindow = self
    self.hide()
    self.ui = ClientRegisterClass(self.windowdata)
    pass


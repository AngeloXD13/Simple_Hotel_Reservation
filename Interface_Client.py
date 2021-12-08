import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

class InterfaceClientClass(QMainWindow):
    def __init__(self):
        super(InterfaceClientClass, self).__init__()

        uic.loadUi("ui/splashscreen.ui", self)

        self.show()

    def keyPressEvent(self, event):
        gotoselection(self)

    def mousePressEvent(self, event):
        gotoselection(self)

def gotoselection(self):
    from Client_selection import ClientSelectionClass
    self.destroy()
    self.ui = ClientSelectionClass()

app = QApplication(sys.argv)
interface = InterfaceClientClass()
app.exec_()

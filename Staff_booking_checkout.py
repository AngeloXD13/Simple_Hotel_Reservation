import sys
from PyQt5.QtWidgets import QDialog, QPushButton, QLabel, QLineEdit, QDateEdit, QTimeEdit, QRadioButton, QCheckBox, QSpinBox, QTextBrowser
from PyQt5 import uic

class StaffBookingCheckoutClass(QDialog):
    def __init__(self, windowData):
        super(StaffBookingCheckoutClass, self).__init__()
        self.windowData = windowData

        uic.loadUi("ui/staff_booking_checkout.ui", self)
        self.show()

        self.creditcard_rb = self.findChild(QRadioButton, "credit_rb")
        self.paymaya_rb = self.findChild(QRadioButton, "paymaya_rb")
        self.gcash_rb = self.findChild(QRadioButton, "gcash_rb")
        self.cash_rb = self.findChild(QRadioButton, "cash_rb")

        self.rate_tb = self.findChild(QTextBrowser, "rate_tb")
        self.downpayment_rb = self.findChild(QRadioButton, "downpayment_rb")
        self.fullypaid_rb = self.findChild(QRadioButton, "fullypaid_rb")
        self.totalamount_tb = self.findChild(QTextBrowser, "totalamount_tb")

        self.reserve_btn = self.findChild(QPushButton, "reserve_btn")
        self.exit_btn = self.findChild(QPushButton, "exit_btn")
        self.status_lbl = self.findChild(QLabel, "status_lbl")

        getValues(self)
        self.creditcard_rb.released.connect(lambda: getValues(self))
        self.paymaya_rb.released.connect(lambda: getValues(self))
        self.gcash_rb.released.connect(lambda: getValues(self))
        self.cash_rb.released.connect(lambda: getValues(self))
        self.downpayment_rb.released.connect(lambda: getValues(self))
        self.fullypaid_rb.released.connect(lambda: getValues(self))

        self.exit_btn.clicked.connect(lambda: self.hide())


def getValues(self):

    print("getvalues")

    self.creditcard = self.creditcard_rb.isChecked()
    self.paymaya = self.paymaya_rb.isChecked()
    self.gcash = self.gcash_rb.isChecked()
    self.cash = self.cash_rb.isChecked()
    self.downpayment = self.downpayment_rb.isChecked()
    self.fullypaid = self.fullypaid_rb.isChecked()

    self.status_lbl.setText("Choose Payment Method")

    if self.creditcard == False and self.paymaya == False and self.gcash == False and self.cash == False:
        self.status_lbl.setText("Choose Payment Option")
    elif self.downpayment == False and self.fullypaid == False:
        self.status_lbl.setText("Choose Option")
    else:
        self.paymentMethod = None
        if self.creditcard == True:
            self.paymentMethod = "Credit Card"
        elif self.paymaya == True:
            self.paymentMethod = "PayMaya"
        elif self.gcash == True:
            self.paymentMethod = "GCash"
        elif self.cash == True:
            self.paymentMethod = "Cash"
        self.status_lbl.setText("OK")
        self.reserve_btn.setEnabled(True)




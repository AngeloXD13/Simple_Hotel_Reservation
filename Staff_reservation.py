import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5 import uic
from PyQt5 import QtWidgets

from DATABASE_MANAGER_MYSQL import getAllReservationData

class StaffReservationClass(QMainWindow):
    def __init__(self, windowData):
        super(StaffReservationClass, self).__init__()
        self.windowData = windowData

        uic.loadUi("ui/staff_reservations.ui", self)
        self.exit_btn = self.findChild(QPushButton, "exit_btn")
        self.reservation_tw = self.findChild(QTableWidget, "reservation_tableWidget")

        self.exit_btn.clicked.connect(lambda : gotomenu(self))

        loadallreservationdata(self)
        self.show()

def loadallreservationdata(self):
    items = getAllReservationData()
    print(items)
    tableRow = 0
    self.reservation_tw.setRowCount(1000)
    for item in items:
        self.reservation_tw.setItem(tableRow, 4, QtWidgets.QTableWidgetItem(str(item[0])))
        self.reservation_tw.setItem(tableRow, 0, QtWidgets.QTableWidgetItem(str(item[1])))
        self.reservation_tw.setItem(tableRow, 5, QtWidgets.QTableWidgetItem(str(item[2]))) #checkin
        self.reservation_tw.setItem(tableRow, 6, QtWidgets.QTableWidgetItem(str(item[4]))) #checkout
        self.reservation_tw.setItem(tableRow, 7, QtWidgets.QTableWidgetItem(str(item[15])))#room id
        self.reservation_tw.setItem(tableRow, 8, QtWidgets.QTableWidgetItem(str(item[16])))#status
        self.reservation_tw.setItem(tableRow, 1, QtWidgets.QTableWidgetItem(str(item[19])))#name
        self.reservation_tw.setItem(tableRow, 2, QtWidgets.QTableWidgetItem(str(item[21])))#address
        self.reservation_tw.setItem(tableRow, 3, QtWidgets.QTableWidgetItem(str(item[20])))#phonenumber
        tableRow = tableRow + 1
        print(tableRow)

def gotomenu(self):
    menu = self.windowData.previousWindow
    self.destroy()
    menu.show()

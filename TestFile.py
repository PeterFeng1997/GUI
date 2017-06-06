import sys
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
import os

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('heaterGUI.ui', self)
        self.setUp()
        self.temp = 0
        self.P_center = 0
        self.I_center = 0
        self.D_center = 0
        self.P_edge = 0
        self.I_edge = 0
        self.D_edge = 0
        #self.show()

    def setUp(self):
        self.outputMessage.setReadOnly(True)
        self.outputMessage.append("test string")
        self.outputMessage.append('[Time: ' + "a]" + '[Temp_1: ' + "b]" + '[Temp_2: ' + "c]" + '\n[Duty_center: ' +"d]" + '[Duty_edge: ' + "e]")
        self.runButton.clicked.connect(self.handleRun)

    def handleRun(self):
        statusTemp = self.checkTemp()
        if(statusTemp == "enter a temperature"):
            self.generateMessageBox("Enter Temperature", "Please enter a temperature value")
        elif(statusTemp == "temperature too high"):
            self.generateMessageBox("Temperature too high", "The temperature value entered is too high. Please enter a value below 200.")
        elif(statusTemp == "invalid temperature"):
            self.generateMessageBox("Invalid temperature", "Please enter a valid temperature")
        elif(statusTemp  == "valid temperature"):
            statusP_center = self.checkP("center")
            statusI_center = self.checkI("center")
            statusD_center = self.checkD("center")

            statusP_edge = self.checkP("edge")
            statusI_edge = self.checkI("edge")
            statusD_edge = self.checkD("edge")

            if(statusP_center == "invalid P"):
                self.generateMessageBox("Invalid center P", "The center P value entered is invalid. Please enter a valid value")
            elif(statusP_center == "enter a P"):
                self.generateMessageBox("Enter center P value", "Please enter a center P value.")

            if(statusI_center == "invalid I"):
                self.generateMessageBox("Invalid center I", "The center I value entered is invalid. Please enter a valid value")
            elif(statusI_center == "enter a I"):
                self.generateMessageBox("Enter center I value", "Please enter a center I value.")

            if(statusD_center == "invalid D"):
                self.generateMessageBox("Invalid D", "The center D value entered is invalid. Please enter a valid value")
            elif(statusD_center == "enter a D"):
                self.generateMessageBox("Enter center D value", "Please enter a center D value.")


            if(statusP_edge == "invalid P"):
                self.generateMessageBox("Invalid edge P", "The edge P value entered is invalid. Please enter a valid value")
            elif(statusP_edge == "enter a P"):
                self.generateMessageBox("Enter edge P value", "Please enter an edge P value.")

            if(statusI_edge == "invalid I"):
                self.generateMessageBox("Invalid edge I", "The edge I value entered is invalid. Please enter a valid value")
            elif(statusI_edge == "enter a I"):
                self.generateMessageBox("Enter edge I value", "Please enter an edge I value.")

            if(statusD_edge == "invalid D"):
                self.generateMessageBox("Invalid D", "The edge D value entered is invalid. Please enter a valid value")
            elif(statusD_edge == "enter a D"):
                self.generateMessageBox("Enter edge D value", "Please enter an edge D value.")

            if(statusP_center == "valid P" and statusI_center == "valid I" and statusD_center == "valid D"):
                center_Valid = True
            else:
                center_Valid = False

            if (statusP_edge == "valid P" and statusI_edge == "valid I" and statusD_edge == "valid D"):
                edge_Valid = True
            else:
                edge_Valid = False

            if(center_Valid == True and edge_Valid == True):
                self.temp = float(self.tempEdit.text())
                self.P_center = float(self.pEdit_center.text())
                self.I_center = float(self.iEdit_center.text())
                self.D_center = float(self.dEdit_center.text())
                self.P_edge = float(self.pEdit_edge.text())
                self.I_edge = float(self.iEdit_edge.text())
                self.D_edge = float(self.dEdit_edge.text())

    def generateMessageBox(self, title, msg):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgBox.setText(msg)
        msgBox.exec_()

    def checkTemp(self):
        if (self.tempEdit.text() != ''):
            if (self.isTextNumber(self.tempEdit.text()) == True):
                if (float(self.tempEdit.text()) > 200):
                    return("temperature too high")  # output that the input is too high
                else:
                    return("valid temperature")
            else:
                return("invalid temperature")
        else:
            return("enter a temperature")

    def checkP(self, location):
        if(location == "center"):
            textBox = self.pEdit_center
        elif(location == "edge"):
            textBox = self.pEdit_edge
        if(textBox.text() != ''):
            if(self.isTextNumber(textBox.text()) == True):
                return("valid P")
            else:
                return("invalid P")
        else:
            return("enter a P")

    def checkI(self, location):
        if(location == "center"):
            textBox = self.iEdit_center
        elif(location == "edge"):
            textBox = self.iEdit_edge
        if(textBox.text() != ''):
            if(self.isTextNumber(textBox.text()) == True):
                return("valid I")
            else:
                return("invalid I")
        else:
            return("enter a I")

    def checkD(self, location):
        if(location == "center"):
            textBox = self.dEdit_center
        elif(location == "edge"):
            textBox = self.dEdit_edge
        if(textBox.text() != ''):
            if(self.isTextNumber(textBox.text()) == True):
                return("valid D")
            else:
                return("invalid D")
        else:
            return("enter a D")

    def isTextNumber (self, input):
        try:
            int(input)
            return True
        except ValueError:
            return False

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


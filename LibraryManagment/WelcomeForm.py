from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class WelcomeClass(QDialog):
    def __init__(self):
        super(WelcomeClass,self).__init__()
        uic.loadUi('WelcomeScreen.ui',self)
        self.startBut.clicked.connect(self.StartProcess)

    def StartProcess(self):
        from LoginCheck import Login_Form_Class
        lg=Login_Form_Class()
        self.setVisible(False)
        lg.show()
        lg.exec_()

app=QApplication(sys.argv)
welcome=WelcomeClass()
welcome.show()
sys.exit(app.exec_())
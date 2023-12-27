#edited
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5 import QtWidgets,uic
import mysql.connector as c

class Login_Form_Class1(QDialog):
   

    def __init__(self):
        super(Login_Form_Class1,self).__init__()
        uic.loadUi('loginform.ui',self)
        self.logo.setStyleSheet("background-image:url(logophoto.jpg);")
        self.loginBut.clicked.connect(self.LoginProcesss)
        self.closeBut.clicked.connect(self.CloseProcess)
        self.mydb=None

    def LoginProcesss(self):
        usr=self.usrTxtBox.toPlainText().strip()
        pwd=self.pwdTxtBox.text().strip()
        print(f"username {usr} and password {pwd}")
        self.CheckLogin(usr,pwd)

    def DBConnect(self):
        try:
            self.mydb=c.connect(
                host="localhost",
                user="root",
                password="root",
                database="library_db1"
            )
        except c.Error as err:
            print("Something went wrong: {}".format(err)) 
    
    def GetUserRole(self,user_id):
        mycursor=self.mydb.cursor()
        mycursor.execute("select role,username from user_info_tb where user_id="+str(user_id))
        value=mycursor.fetchall()
        role=None
        name=None
        for x in value:
            role=x[0]
            name=x[1]

        return role,name

    def CheckLogin(self,usr,pwd):  
        self.DBConnect()
        mycursor=self.mydb.cursor()
        mycursor.execute("select * from login_tb")
        rows=mycursor.fetchall()
        found=0
        for x in rows:
            if usr==x[1] and pwd==x[2]:
                found=1
                user_id=x[3]
                role,name=self.GetUserRole(user_id)
                if role.lower()=="admin":
                    self.setVisible(False)
                    from AdminProcessForm import AdminInfoProcessForm
                    admin=AdminInfoProcessForm(user_id,role,name)
                    admin.show()
                    admin.exec_()
                else:
                    self.setVisible(False)
                    from StudentTeacherForm import StudentTeacherProcess
                    stu=StudentTeacherProcess(user_id,role,name)
                    stu.show()
                    stu.exec_()
                break
        if found==0:
            from PyQt5.QtWidgets import QMessageBox
            self.usrTxtBox.clear()
            self.pwdTxtBox.clear()
            msg=QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Username and password does not exist. Please try again.")
            msg.setWindowTitle("Login Error")
            msg.setInformativeText("Next Login")
            msg.exec_()

    def CloseProcess(self):
        self.exec_()

if __name__=="__main__":
    app=QApplication(sys.argv)
    login=Login_Form_Class1()
    login.show()
    app.exec_()
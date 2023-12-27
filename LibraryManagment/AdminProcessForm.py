from PyQt5 import uic,QtCore
import sys
from PyQt5.QtWidgets import QApplication,QDialog,QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from PyQt5.QtCore import *
import mysql.connector as c
import pandas as pd

class AdminInfoProcessForm(QDialog):
    def __init__(self,user_id,role,name):
        super(AdminInfoProcessForm,self).__init__()
        uic.loadUi('AdminForm.ui',self)
        self.showBut.clicked.connect(self.showData)
        self.showBookBut.clicked.connect(self.showBookData)
        self.updateBookBut.clicked.connect(self.updateBookData)
        self.mydb=None
        self.setWindowTitle("Show Users")
        self.welcomelbl.setText("Welcome : "+name)

    def showBookData(self):
        self.DBConnect()
        SQL_Query = pd.read_sql_query("select * from book_tb", self.mydb) 
        df = pd.DataFrame(SQL_Query, columns=['id','book_id','title','author','publisher','published_year','num_copies','left_copies'])
        from TableModel import pandasModel
        model = pandasModel(df)
        self.tableView.setModel(model)   

    def updateBookData(self):
        pass

    def showData(self):
        optionChose=None
        if self.regBut.isChecked():
            optionChose="register_user"
        else:
            optionChose="borrow_user"

        usertype=self.userTypeComboBox.currentText()
        usertype=str(usertype).lower()
        self.addDataToTable(optionChose,usertype)

    def ShowRegisterUser(self,usertype):
        if usertype=="all":
            SQL_Query = pd.read_sql_query("select * from user_info_tb", self.mydb)    
        elif usertype=="student":
            SQL_Query = pd.read_sql_query("select * from user_info_tb where role='student'", self.mydb) 
        elif usertype=="teacher":
            SQL_Query = pd.read_sql_query("select * from user_info_tb where role='teacher'", self.mydb)
        elif usertype=="admin":
            SQL_Query = pd.read_sql_query("select * from user_info_tb where role='admin'", self.mydb)
           
        try:
            df = pd.DataFrame(SQL_Query, columns=['user_id', 'username', 'role','department_class','email'])
            from TableModel import pandasModel
            model = pandasModel(df)
            self.tableView.setModel(model)
        except:
            print("Error: unable to convert the data")
            self.mydb.close()

    def addDataToTable(self,optionChose,usertype):
        self.DBConnect()
        #Check User Type
        if optionChose=="register_user":
            self.ShowRegisterUser(usertype)
        else:
            self.ShowBorrowUser(usertype)

    def ShowBorrowUser(self,usertype):  

        mycursor=self.mydb.cursor()
        sqlstr="select user_info_tb.username as Name,user_info_tb.role as Role,user_info_tb.department_class as Department,book_tb.title as BookName,borrow_tb.borrow_date as BorrowDate from user_info_tb,book_tb,borrow_tb where user_info_tb.user_id=borrow_tb.user_id and borrow_tb.book_id=book_tb.book_id;"
        SQL_Query = pd.read_sql_query(sqlstr, self.mydb)   

        usertype=self.userTypeComboBox.currentText()
        usertype=str(usertype).lower()
        df = pd.DataFrame(SQL_Query, columns=['Name', 'Role','Department', 'BookName','BorrowDate'])
      
        if usertype=="student":
            df=df[df['Role'].str.contains('student')]
            print('df')
        elif usertype=="teacher":
            df=df[df['Role'].str.contains('teacher')]
           
        elif usertype=="admin":
            df=df[df['Role'].str.contains('admin')]
        
        from TableModel import pandasModel
        model = pandasModel(df)
        self.tableView.setModel(model)

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
     

"""app=QApplication(sys.argv)
stu=AdminInfoProcessForm()
stu.show()
app.exec_()"""
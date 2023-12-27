from PyQt5 import uic,QtCore
import sys
from PyQt5.QtWidgets import QApplication,QDialog,QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from PyQt5.QtCore import *
import mysql.connector as c
import pandas as pd

class AdminInfoProcessForm1(QDialog):
    def __init__(self,user_id,role,name):
        super(AdminInfoProcessForm1,self).__init__()
        uic.loadUi('AdminForm.ui',self)
        self.welcomelbl.setText("Welcome "+name)
        self.showBut.clicked.connect(self.showData)
        self.showBookBut.clicked.connect(self.showBookData)
        self.updateBookBut.clicked.connect(self.updateBookData)
        self.tableView.clicked.connect(self.TableSelect)
        self.mydb=None

    def TableSelect(self):
        self.updateBookBut.setEnabled(True)
        
    def showBookData(self):
        self.DBConnect()
        SQL_Query = pd.read_sql_query("select * from book_tb", self.mydb) 
        df = pd.DataFrame(SQL_Query, columns=['id','book_id','title','author','publisher','published_year','num_copies','left_copies'])
        from TableModel import pandasModel
        model = pandasModel(df)
        self.tableView.setModel(model) 

    def updateBookData(self):
        index=self.tableView.selectionModel().currentIndex()
        value=index.sibling(index.row(),index.column()).data()
        from CURDBookProcess import CRUDProcess
        crud=CRUDProcess(value)
        crud.show()
        crud.exec_()


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

    def GetData(self):
        useroption=None
        if self.regBut.isChecked():
            useroption="register_user"
        else:
            useroption="borrow_user"
        combodata=self.userTypeComboBox.currentText()
        return useroption,combodata

    def showData(self):
        useroption,combodata=self.GetData()
        combodata=combodata.lower()
        if useroption=="register_user":
            self.ShowRegisterUser(combodata)
        else:
            self.ShowBorrowUser(combodata)

    def ShowRegisterUser(self,combodata):
        self.DBConnect()
        cursor=self.mydb.cursor()
        if combodata=="all":
            sqlstr="select * from user_info_tb"
        else:
            sqlstr="select* from user_info_tb where role='"+combodata+"'"
        SQL_Query = pd.read_sql_query(sqlstr, self.mydb)      
        df = pd.DataFrame(SQL_Query, columns=['username','role','email','department_class'])
        from TableModel import pandasModel
        model = pandasModel(df)
        self.tableView.setModel(model)

    def ShowBorrowUser(self,combodata):
        self.DBConnect()
        cursor=self.mydb.cursor()
        if combodata=="all":
            sqlstr="""
            select  User.username as Name,User.role as Role,Book.title as Title, BTB.borrow_date as B_Date
            from borrow_tb as BTB, user_info_tb as User, book_tb as Book
            where BTB.user_id=User.user_id 
            and BTB.book_id=Book.book_id"""
        else:
            sqlstr="""
            select  User.username as Name,User.role as Role,Book.title as Title, BTB.borrow_date as B_Date
            from borrow_tb as BTB, user_info_tb as User, book_tb as Book
            where BTB.user_id=User.user_id 
            and BTB.book_id=Book.book_id
            and User.role='"""+combodata+"'"
        SQL_Query = pd.read_sql_query(sqlstr, self.mydb)      
        df = pd.DataFrame(SQL_Query, columns=['Name','Role','Title','B_Date'])
        from TableModel import pandasModel
        model = pandasModel(df)
        self.tableView.setModel(model)
        

app=QApplication(sys.argv)
stu=AdminInfoProcessForm1(3,"admin","Ko Ko")
stu.show()
app.exec_()
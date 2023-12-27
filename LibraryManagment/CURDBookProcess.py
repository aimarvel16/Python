from PyQt5 import uic,QtCore
import sys
from PyQt5.QtWidgets import QApplication,QDialog,QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from PyQt5.QtCore import *
import mysql.connector as c
import pandas as pd
from PyQt5.QtWidgets import QMessageBox

class CRUDProcess(QDialog):
    def __init__(self,book_id):
        super(CRUDProcess,self).__init__()
        uic.loadUi('CRUDBookForm.ui',self)
        self.LoadData(book_id)
        self.setWindowTitle("Updat Book Information")
        self.mydb=None
        self.updateBut.clicked.connect(self.UpdateData)
        self.newBut.clicked.connect(self.InsertData)
        self.deleteBut.clicked.connect(self.DeleteData)
        self.clearBut.clicked.connect(self.ClearData)

    def ClearData(self):
        self.txtID.clear()
        self.txtName.clear()
        self.txtAuthor.clear()
        self.txtPublisher.clear()
        self.txtYear.clear()
        self.txtCopy.clear()
        self.txtLeft.clear()
        self.txtID.setEnabled(True)

    def InsertData(self):
        bid=self.txtID.toPlainText()
        if len(bid)<1:
            QMessageBox.about(self, "Entry Data", "Please Enter Book Id that you want to insert")
        else:
            result=self.SearchID(bid)
            if result==False:
                QMessageBox.about(self, "Duplicate Book ID", "Please Enter Another Book Id for New Book.")
            else:
                book_name=self.txtName.toPlainText()
                author=self.txtAuthor.toPlainText()
                publisher=self.txtPublisher.toPlainText()
                year=self.txtYear.toPlainText()
                copy=self.txtCopy.toPlainText()
                left_copy=self.txtLeft.toPlainText()
                self.DBConnect()
                cursor=self.mydb.cursor()
                sqlstr="insert into book_tb(book_id,title,author,publisher,published_year,num_copies,left_copies) values(%s,%s,%s,%s,%s,%s,%s)"
                val=(str(bid),book_name,author,publisher,year,copy,left_copy)
                cursor.execute(sqlstr,val)
                self.mydb.commit()
                QMessageBox.about(self, "Success", "Your data is inserted successfully.")


    def UpdateData(self):
        self.txtID.setEnabled(True)

        bid=self.txtID.toPlainText()
        book_name=self.txtName.toPlainText()
        author=self.txtAuthor.toPlainText()
        publisher=self.txtPublisher.toPlainText()
        year=self.txtYear.toPlainText()
        copy=self.txtCopy.toPlainText()
        left_copy=self.txtLeft.toPlainText()
        self.DBConnect()
        cursor=self.mydb.cursor()

        sqlstr="update book_tb set title='"+book_name+"', author='"+author+"', publisher='"+publisher+"', published_year='"+year+"', num_copies="+str(copy)+", left_copies="+str(left_copy)+" where book_id="+str(bid)
        print(sqlstr)
        cursor.execute(sqlstr)
        self.mydb.commit()
        print(cursor.rowcount," records affected.")
        QMessageBox.about(self, "Success", "Your Data are updated successfully.")

    def DeleteData(self):
        self.DBConnect()
        bid=self.txtID.toPlainText()
        if len(bid)<1:
            QMessageBox.about(self, "Entry Data", "Please Enter Book Id that you want to delete")
        else:
            result=self.SearchID(bid)
            if result==True:
                QMessageBox.about(self, "No Data Found", "Please Enter Another Book ID that you want to delete")
            else:
                cursor=self.mydb.cursor()
                sqlstr="delete from book_tb where book_id="+str(bid)
                cursor.execute(sqlstr)
                self.mydb.commit()
                QMessageBox.about(self, "Success", "Your book is delted successfully.")
        self.ClearData()

    def SearchID(self,bid):
        signal=False
        self.DBConnect()
        cursor=self.mydb.cursor()
        sqlstr='select * from book_tb where book_id='+str(bid)
        cursor.execute(sqlstr)
        result=cursor.fetchone()
        if result==None:
            signal=True
        return signal



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


    def LoadData(self,bid):
        self.DBConnect()
        cursor=self.mydb.cursor()
        sqlstr="select * from book_tb where book_id="+str(bid)
        cursor.execute(sqlstr)
        result=cursor.fetchone()
        self.txtID.setPlainText(str(result[1]))
        self.txtName.setPlainText(str(result[2]))
        self.txtAuthor.setPlainText(str(result[3]))
        self.txtPublisher.setPlainText(str(result[4]))
        self.txtYear.setPlainText(str(result[5]))
        self.txtCopy.setPlainText(str(result[6]))
        self.txtLeft.setPlainText(str(result[7]))
        self.txtID.setEnabled(False)

"""app=QApplication(sys.argv)
stu=CRUDProcess(1001)
stu.show()
app.exec_()"""
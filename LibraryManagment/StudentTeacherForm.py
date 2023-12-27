from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QApplication
import mysql.connector as c
import pandas as pd
from PyQt5.QtWidgets import QMessageBox

class StudentTeacherProcess(QDialog):
    def __init__(self,id,role,name):
        super(StudentTeacherProcess,self).__init__()
        uic.loadUi('StudentForm.ui',self)
        if role=="teacher":
            self.welcomelbl.setText("Welcome teacher, "+name)
        else:
            self.welcomelbl.setText("Welcome student, "+name)
        self.id=id
        self.role=role
        self.name=name
        self.searchBut.clicked.connect(self.SearchBut)
        self.borrowBut.clicked.connect(self.BorrowBut)
        self.checkBut.clicked.connect(self.SeeBooks)
        self.mydb=None

    def GetData(self):
        useroption=None
        if self.author_rbut.isChecked():
            useroption="author"
        elif self.title_rbut.isChecked():
            useroption="title"
        else:
            useroption="published_year"
        
        inputdata=self.inputTxt.toPlainText()
        return useroption,inputdata

    def SearchBut(self):
        useroption,inputdata=self.GetData()
        self.BookSearch(useroption,inputdata)

    def BookSearch(self,useroption,inputdata):
        inputdata=inputdata.strip()
        if len(inputdata)==0:
            QMessageBox.about(self, "No Data", "Please type what you want to search.")
        else:
            self.DBConnect()
            cursor=self.mydb.cursor()
            sqlstr="select * from book_tb where "+useroption+"='"+inputdata+"'"
            SQL_Query = pd.read_sql_query(sqlstr, self.mydb)  
            all_df=pd.DataFrame(SQL_Query, columns=['book_id','title','author','published_year','left_copies'])
            df = pd.DataFrame(SQL_Query, columns=['book_id','title','author','published_year'])
            if len(df)<1:
                QMessageBox.about(self, "No Found", "The data you search is not found.")

            from TableModel import pandasModel
            model = pandasModel(df)
            self.tableView.setModel(model)
            return all_df
    
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


    def BorrowBut(self):
        useroption,inputdata=self.GetData()
        if len(inputdata)<1:
            QMessageBox.about(self, "No Data", "Enter the data.")
            useroption,inputdata=self.GetData()
        else:
            df=self.BookSearch(useroption,inputdata)
            left_copy=list(df['left_copies'])
            left_copy=int(left_copy[0])
            if left_copy<1:
                QMessageBox.about(self, "No Copies Left", "Please try another book.")
            else:
                reply = QMessageBox.question(self, 'Quit', 'Are you sure to borrow this book?',
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                #count minus to book_tb
                self.minusBook(df)
                #add information to borrow_tb
                self.updateBorrowBook(df)
                QMessageBox.about(self, "Dear "+self.name, "The book is already borrowed by you. Can go to receptions to take the book.")

    def updateBorrowBook(self,df):
        book_id=int(df.loc[0,"book_id"])
        user_id=self.id
        from datetime import date
        today = date.today()
        cursor=self.mydb.cursor()
        sql="insert into borrow_tb(user_id,book_id,borrow_date) values(%s,%s,%s)"
        val=(user_id,book_id,str(today))
        cursor.execute(sql,val)
        self.mydb.commit()
        print(cursor.rowcount," records affected into Borrow table.")

    def minuBook(self,df):
        copy_num=int(df.loc[0,'left_copies'])
        copy_num=copy_num-1
        book_id=int(df.loc[0,'book_id'])
        cursor=self.mydb.curosr()
        sqlstr="update book_tb set left_copies="+str(copy_num)+" where book_id="+str(book_id)
        print(sqlstr)
        cursor.execute(sqlstr)
        self.mydb.commit()
        print(cursor.rowcount," records affected into book table.")

    def updateBorrowBook(self,df):
        pass

    def SeeBooks(self):
        #self.user_id
        self.DBConnect()
        curosr=self.mydb.cursor()
        sqlstr="select B.title, B.author, BTB.borrow_date from borrow_tb as BTB, book_tb as B where BTB.user_id="+str(self.id)+" and BTB.book_id=B.book_id"
        print(sqlstr)
        SQL_Query = pd.read_sql_query(sqlstr, self.mydb)  
        df = pd.DataFrame(SQL_Query, columns=['title','author','borrow_date'])
        if len(df)<1:
            QMessageBox.about(self, "No Found", "You have not borrowed any book yet.")

        from TableModel import pandasModel
        model = pandasModel(df)
        self.tableView.setModel(model)
    
"""app=QApplication(sys.argv)
#stu=StudentTeacherProcess(3,'student','Soe Myint')
stu=StudentTeacherProcess(2,'teacher','Moe Moe Thein')
stu.show()
app.exec_()"""

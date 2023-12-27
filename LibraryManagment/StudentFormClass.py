from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QApplication
import mysql.connector as c
import pandas as pd
from PyQt5.QtWidgets import QMessageBox

class StudentProcess(QDialog):
    def __init__(self,id,role,name):
        super(StudentProcess,self).__init__()
        uic.loadUi('StudentForm.ui',self)
        self.welcomelbl.setText("Hello , "+name)
        self.user_id=id
        self.role=role
        self.name=name
        self.searchBut.clicked.connect(self.SearchBut)
        self.borrowBut.clicked.connect(self.BorrowBut)
        self.checkBut.clicked.connect(self.SeeBooks)
        self.mydb=None

    def SeeBooks(self):
        self.DBConnect()
        mycursor=self.mydb.cursor()
        sqlstr="select  b.title as Title,b.author as Author, br.borrow_date as B_Date from book_tb as b, borrow_tb as br where br.book_id=b.book_id and user_id="+str(self.user_id);
        SQL_Query = pd.read_sql_query(sqlstr, self.mydb)   
        df = pd.DataFrame(SQL_Query, columns=['Title','Author','B_Date'])
        if len(df)<1:
            QMessageBox.about(self, "No Found", "The data you search is not found.")

        from TableModel import pandasModel
        model = pandasModel(df)
        self.tableView.setModel(model)
        return df

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
        option_name,search_data=self.GetInputData()
        if len(search_data)<1:
            QMessageBox.about(self, "No Data", "Enter the data.")
            option_search,search_data=self.GetInputData()
        else:
            df=self.BookSearch(option_name,search_data)

            left_copy=list(df['left_copies'])
            left_copy=left_copy[0]
            
            if len(df)>0 and left_copy!=0:
                reply = QMessageBox.question(self, 'Quit', 'Are you sure to borrow this book?',
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                QMessageBox.about(self, "Dear "+self.name, "The book is already borrowed by you. Can go to receptions to take the book.")
                #minus the left copy in borrow_table
                #change book_table and borrow_table
                self.MinuBookInBookTable(df)
                #Add Data into Borrow Table
                self.AddInfoBorrowTable(df)

    def AddInfoBorrowTable(self,df):
        #borrow_tb
        #id,user_id,book_id,borrow_date
        b_id=int(df.loc[0,'book_id'])
        from datetime import date
        today = date.today()
        cursor=self.mydb.cursor()
        sql="insert into borrow_tb(user_id,book_id,borrow_date) values(%s,%s,%s)";
        val=(self.user_id,b_id,str(today))
        cursor.execute(sql,val)
        self.mydb.commit()
        print(cursor.rowcount," records affected into Borrow table.")

    def MinuBookInBookTable(self,df):
        #book_tb
        #id,book_id,title,author,publisher,published_year,num_copies,left_copies
        b_id=int(df.loc[0,'book_id'])
        copy_count=int(df.loc[0,'left_copies'])
        copy_count=copy_count-1
        cursor=self.mydb.cursor()
        sql="update book_tb set left_copies="+str(copy_count)+" where book_id="+str(b_id);
        print("SQL ")
        print(sql)
        cursor.execute(sql)
        self.mydb.commit()
        print(cursor.rowcount," records affected into book table.")
        #Show Updated data into TableView
        self.BookSearchByChangeID(b_id)
        

    def GetInputData(self):
        option_search=None
        if self.author_rbut.isChecked():
            option_search="author"
        elif self.title_rbut.isChecked():
            option_search="title"
        elif self.year_rbut.isChecked():
            option_search="published_year"
        
        #text data
        search_data=self.inputTxt.toPlainText().strip()
        return option_search,search_data

    def SearchBut(self):
        #option choose
        option_search,search_data=self.GetInputData()
        self.BookSearch(option_search,search_data)

    def BookSearchByChangeID(self,id):
        mycursor=self.mydb.cursor()
        sqlstr="select * from book_tb where book_id="+str(id);
        SQL_Query = pd.read_sql_query(sqlstr, self.mydb)   
        df = pd.DataFrame(SQL_Query, columns=['title','author','publisher','published_year','left_copies','book_id'])
        if len(df)<1:
            QMessageBox.about(self, "No Found", "The data you search is not found.")

        from TableModel import pandasModel
        model = pandasModel(df)
        self.tableView.setModel(model)

    def BookSearch(self,option_name,search_data):
        self.DBConnect()
        mycursor=self.mydb.cursor()
        sqlstr="select * from book_tb where "+option_name+"='"+search_data+"'";
        SQL_Query = pd.read_sql_query(sqlstr, self.mydb)   
        df = pd.DataFrame(SQL_Query, columns=['title','author','publisher','published_year','left_copies','book_id'])
        if len(df)<1:
            QMessageBox.about(self, "No Found", "The data you search is not found.")

        from TableModel import pandasModel
        model = pandasModel(df)
        self.tableView.setModel(model)
        return df

"""app=QApplication(sys.argv)
stu=StudentProcess(3,'student','Soe Myint')
stu.show()
app.exec_()"""

from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import tabula
import csv
import re

import xlrd
import mysql.connector
import parse
import pandas as pd
import datetime
import time
from collections import namedtuple
from mysql.connector import Error



							#file i.py Teacher list entry to database
class uptlist(Frame):
	i=0
	def __init__(self,user,key,db,master=None):
		super().__init__(master)
		self.uname=user
		self.pas=key
		self.dbname=db
		self.design()
		self.grid()
		self.filename=''
		#self.browsefunc()
		self.msg1()
		self.browseButton()
		
		
		self.submit()
		#self.path()
		
	def design(self):
		self.master.grid_rowconfigure(0, weight=1)
		self.master.grid_rowconfigure(2, weight=1)
		self.master.grid_columnconfigure(0, weight=1)
		self.master.grid_columnconfigure(4, weight=1)
		self.master.geometry('1000x400')
		self.master.title("Upload Teacher List")

	def browsefunc(self):
		self.master.protocol("WM_DELETE_WINDOW",lambda:self.on_exit(0))
		pathlabel = Label(self.master)
		fileoptions = dict(defaultextension=".xls", initialdir="/home/aks/Desktop/Project",filetypes=[('Excel file', '*.xls')])
		self.filename = filedialog.askopenfilename(parent=self.master,**fileoptions)
		if(self.filename):
			uptlist.i=1
		else:
			uptlist.i=0	
		pathlabel.config(text=self.filename)			##Filename is path to select the file
		pathlabel.grid(row=1,column=3)
		self.master.protocol("WM_DELETE_WINDOW",lambda:self.on_exit(1))
	def on_exit(self,i):
			if(i==0):
				print("Sorry")
			else:
				self.master.destroy()


	def msg1(self):
		msg="Browse the Teacher list "
		w=Label(self.master,text=msg)
		w.grid(row=1, column=1, sticky=W) 

	def browseButton(self):
		self.browsebutton = Button(self.master, text="Browse", command=lambda:uptlist.browsefunc(self))
		self.browsebutton.grid(row=1, column=2)
	
	
		
	def sett():
		print (uptlist.var1.get())			#use of sem to be done here 

	def submit(self):
		sbt=Button(self.master,text="Submit",command=lambda:uptlist.strt(self))
		sbt.grid(row=2,column=2)
		sbt1=Button(self.master,text="Close",command=lambda:self.master.destroy())
		sbt1.grid(row=2, column=1)

	def upload(self):
			if(self.uname!='' and self.pas!='' and self.dbname!=''):
				try:
					mydb = mysql.connector.connect( host="localhost",  user=self.uname, passwd=self.pas,database=self.dbname)
					if mydb.is_connected():
						cur = mydb.cursor(prepared=True)
	    			#cur = mydb.cursor(prepared=True)
						print("ok1"+self.filename)
						cur.execute("DROP TABLE IF EXISTS teachers;")
						cur.execute("CREATE TABLE teachers(tid int(3),Name varchar(50),Mobile_no bigint(10),Email varchar(30),Department varchar(20),Status varchar(15),availibility char(2))")
						book1=xlrd.open_workbook(self.filename)#excel2="course12 (1).xlsx"
						sheet=book1.sheet_by_index(0)
    
						for r in range(1,sheet.nrows):
							
							sql_insert_query1 = """ INSERT INTO teachers(tid, Name, Mobile_no, Email,Department,Status,availibility) VALUES (%s, %s, %s, %s, %s, %s,'I')"""
							
							a=sheet.cell(r,0).value
							
							b= sheet.cell(r,1).value
							
							c= sheet.cell(r,2).value
							
							d= sheet.cell(r,3).value
							
							e= sheet.cell(r,4).value
						
							f= sheet.cell(r,5).value
							
							
							insert_tuple_2 = (a,b,c,d,e,f)
							
							cur.execute(sql_insert_query1, insert_tuple_2)
							
							mydb.commit()
							
							print("Data inserted successfully into teachers table using the prepared statement")
								



					
				except mysql.connector.Error as error:
    
					print("parameterized query failed {}".format(error))
					
				finally:
					
					if (mydb.is_connected()):
						
						cur.close()
						
						mydb.close()
						
						print("MySQL connection is closed")

	def strt(self):
		if(uptlist.i!=0):
			self.browsebutton["state"]="disabled"
			self.upload()
			self.master.destroy()
			'''self.e1["state"]="disabled"
			self.e2["state"]="disabled"'''
#	   	  start database():

#	def databased(self): 				# conversion from pdf to csv to be done here
		
#root= Tk()		


#obj1=uptlist(master=root)


#mainloop()

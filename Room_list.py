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


#root = Tk()
							#file j.py Room list entry to database(complete)
class uproomlist(Frame):
	
	i=0
	def __init__(self,user,key,db,master=None):
		super().__init__(master)
		self.uname=user
		self.pas=key
		self.dbname=db
		self.filename=''
		self.grid()
		self.msg1()
		self.browseButton()
		self.submit()
		self.design()
	
	def design(self):
		self.master.geometry('1000x400')
		self.master.title('Upload Room Capacity')
		self.master.grid_rowconfigure(0, weight=1)
		self.master.grid_rowconfigure(1, weight=1)
		self.master.grid_rowconfigure(2, weight=1)
		self.master.grid_rowconfigure(3, weight=1)
		self.master.grid_columnconfigure(0, weight=1)
		#self.master.grid_columnconfigure(1, weight=1)
		#self.master.grid_columnconfigure(2, weight=1)
		self.master.grid_columnconfigure(3, weight=1)
                

	def browsefunc(self):
		self.master.protocol("WM_DELETE_WINDOW",lambda:self.on_exit(0))	
		pathlabel = Label(self.master)
		fileoptions = dict(defaultextension=".xls", initialdir="/home/aks/Desktop/Project",filetypes=[('Excel file', '*.xls')])
		self.filename = filedialog.askopenfilename(parent=self.master,**fileoptions)
		if(self.filename):
			uproomlist.i=1
		else:
			uproomlist.i=0			
		pathlabel.config(text=self.filename)						##Filename is path to select the file
		pathlabel.grid(row=1,column=3,columnspan=3)
		self.master.protocol("WM_DELETE_WINDOW",lambda:self.on_exit(1))
	
	def on_exit(self,i):
			if(i==0):
				print("Sorry")
			else:
				self.master.destroy()

	
	def msg1(self):
		msg="Select the Room list"
		w=Label(self.master,text=msg)
		w.grid(row=1, column=1) 

	def browseButton(self):
		self.browsebutton = Button(self.master, text="Browse", command=lambda:uproomlist.browsefunc(self))
		self.browsebutton.grid(row=1, column=2, padx=30)

	def upload(self):
		if(self.uname!='' and self.pas!='' and self.dbname!=''):
				try:
					mydb = mysql.connector.connect( host="localhost",  user=self.uname, passwd=self.pas,database=self.dbname)
					if mydb.is_connected():
						cur = mydb.cursor(prepared=True)
	    			#cur = mydb.cursor(prepared=True)
						print("ok1"+self.filename)
						cur.execute("DROP TABLE IF EXISTS room_data;")
						cur.execute("CREATE TABLE room_data(Sno int(3),RNo int(5),Capacity int(10),`Row` int(5));")
						book4=xlrd.open_workbook(self.filename)
						sheet=book4.sheet_by_index(0)
						for r in range (1,sheet.nrows):
							if sheet.cell(r,0).value=="Sr.No." or len(str(sheet.cell(r,0).value))==0:
								x=1
							else:
								sql_insert_query4=""" INSERT INTO room_data(Sno,Rno,Capacity,`Row`) VALUES (%s,%s,%s,%s)"""
								a=sheet.cell(r,0).value 
								b=sheet.cell(r,1).value 
								c=sheet.cell(r,2).value 
								d=sheet.cell(r,3).value
								insert_tuple_5=(a,b,c,d)
								cur.execute(sql_insert_query4,insert_tuple_5)
								mydb.commit()
								print("data inserted into room successfully")
						
				except mysql.connector.Error as error:
    
					print("parameterized query failed {}".format(error))
					
				finally:
					
					if (mydb.is_connected()):
						
						cur.close()
						
						mydb.close()
						
						print("MySQL connection is closed")


	def submit(self):
		sbt=Button(self.master,text="Submit",command=lambda:uproomlist.strt(self))
		sbt.grid(row=2, column=2)
		sbt1=Button(self.master,text="Close",command=lambda:self.master.destroy())
		sbt1.grid(row=2, column=1)
		
	def strt(self):
		if(uproomlist.i!=0):
			self.upload()
			self.master.destroy()
#	   	  start database():

#	def databased(self): 				
		
		


#obj1=uproomlist(master=root)


#mainloop()

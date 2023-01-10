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



class updatesheet(Frame):

												
		def __init__(self,user,key,db,master=None):
			super().__init__(master)
			self.design()
			self.uname=user
			self.pas=key
			self.dbname=db
			self.sem =StringVar()
			self.filename=''
			self.grid()
			self.i=0
			self.msg1()
			self.browseButton()
			self.submit()
			self.label2()
		
			

			
		def design(self):
			self.master.geometry('1000x400')
			self.master.title("Upload Datesheet")
			self.master.grid_rowconfigure(0, weight=1)
			self.master.grid_rowconfigure(1, weight=1)
			self.master.grid_rowconfigure(2, weight=1)
			self.master.grid_rowconfigure(3, weight=1)
			self.master.grid_rowconfigure(4, weight=1)
			self.master.grid_rowconfigure(5, weight=1)
			self.master.grid_columnconfigure(0, weight=1)
			self.master.grid_columnconfigure(5, weight=1)
			
		def browsefunc(self):
			self.master.protocol("WM_DELETE_WINDOW",lambda:self.on_exit(0))
			pathlabel = Label(self.master)
			fileoptions = dict(defaultextension=".xls", initialdir=".",filetypes=[('Excel 		file',	'*.xls')])
			self.filename = filedialog.askopenfilename(parent=self.master,**fileoptions)
			if(self.filename):
				self.i=1
			else:
				self.i=0			
			pathlabel.config(text=self.filename)			##Filename is path to select the file
			pathlabel.grid(row=1,column=3,columnspan=3)
			self.master.protocol('WM_DELETE_WINDOW', lambda:self.on_exit(1))

		def on_exit(self,i):
			if(i==0):
				print("Sorry")
			else:
				self.master.destroy()	
		
		def msg1(self):
			msg="Select the File "
			w=Label(self.master,text=msg)
			w.grid(row=1, column=2) 
	
		def browseButton(self):
			self.browsebutton = Button(self.master,text="Browse", command=lambda:updatesheet.browsefunc(self))
			self.browsebutton.grid(row=1, column=3)
		
		
		def label2(self):
			label = Label( self.master,text = "UPLOAD DATESHEET EXCEL FILE")
			label.place(relx = 0.5, rely = 0.05, anchor = 'n')
	
		def upload(self):
			
			if(self.uname!='' and self.pas!='' and self.dbname!=''):
				try:
					mydb = mysql.connector.connect( host="localhost",  user=self.uname, passwd=self.pas,database=self.dbname)
					if mydb.is_connected():
						cur = mydb.cursor(prepared=True)
	    			#cur = mydb.cursor(prepared=True)
						print("ok1"+self.filename)
						cur.execute("DROP TABLE IF EXISTS course;")
						cur.execute("CREATE TABLE course (Course_Code int(20),Year char(6),Semester char(6),Paper_Code int(9),Paper_Name varchar(150),Sum int(6),Date date,Session varchar(50))")
						book2=xlrd.open_workbook(self.filename)#excel2="course12 (1).xlsx"
						name=["Sheet1","Sheet2","Sheet3"]
						for i in range(0,len(name)):
							sheet=book2.sheet_by_name(name[i])
							sql_insert_query2 = """ INSERT INTO course(Course_Code,Year,Semester,Paper_Code,Paper_Name,Sum,Date,Session) VALUES (%s, %s, %s,%s, %s, %s,%s,%s)"""

							for r in range(1,sheet.nrows):

								if sheet.cell(r,0).value=="Sr. No." or len(str(sheet.cell(r,0).value))==0:

									x=1

								else:
									a=sheet.cell(r,1).value

									b=sheet.cell(r,2).value

									c=sheet.cell(r,3).value

									d=sheet.cell(r,4).value 

									e=sheet.cell(r,5).value

									f=sheet.cell(r,6).value

									g=sheet.cell_value(r,7)

									h=sheet.cell(r,8).value

									date_converter= xlrd.xldate_as_tuple(float(g),book2.datemode)

									print_date=datetime.datetime(*date_converter).strftime("%Y-%m-%d")

									insert_tuple_3 = (a,b,c,d,e,f,print_date,h)

									cur.execute(sql_insert_query2, insert_tuple_3)

									mydb.commit()
									print("Data inserted into course successfully")
			



					
				except mysql.connector.Error as error:
    
					print("parameterized query failed {}".format(error))
					
				finally:
					
					if (mydb.is_connected()):
						
						cur.close()
						
						mydb.close()
						
						print("MySQL connection is closed")
														
		def submit(self):
			sbt=Button(self.master,text="Submit",command=lambda:updatesheet.strt(self))
			sbt.grid(row=2, column=3)
			sbt1=Button(self.master,text="Close",command=lambda:self.master.destroy())
			sbt1.grid(row=2, column=2)
			
		def strt(self):
		
			if(self.i!=0 ):
				self.upload()
				self.master.destroy()
				
	#	   	  start database():
			else:
				print("Time is incorrect")
		
	#	def databased(self): 	

#root=Tk() 
#obj1=updatesheet(master=root)
	#root.attributes('-topmost',True)
	#root.focus_force()
	#root.bind('FocusIn', OnFocusIn)
#mainloop()	
#return obj1.sem.get(), obj1.slot.get()
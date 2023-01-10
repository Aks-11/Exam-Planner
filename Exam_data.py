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
							#file k.py Exam Data entry to database(complete)
class upexamdata(Frame):
	i=0
	def __init__(self,user,key,db,master=None):
		super().__init__(master)
		self.design()
		self.uname=user
		self.pas=key
		self.filename=''
		self.dbname=db
		self.grid()
		self.msg1()
		self.browseButton()
		self.submit()
	
	def design(self):
		self.master.geometry('1000x400')
		self.master.title('Upload Exam Data')
		self.master.grid_rowconfigure(0, weight=1)
		self.master.grid_rowconfigure(3, weight=1)
		self.master.grid_columnconfigure(0, weight=1)
		self.master.grid_columnconfigure(3, weight=1)
		
	def browsefunc(self):
		self.master.protocol("WM_DELETE_WINDOW",lambda:self.on_exit(0))
		pathlabel = Label(self.master)
		fileoptions = dict(defaultextension=".xls", initialdir="/home/aks/Desktop/Project",filetypes=[('Excel file', '*.xls')])
		self.filename = filedialog.askopenfilename(parent=self.master,**fileoptions)
		if(self.filename):
			upexamdata.i=1
		else:
			upexamdata.i=0			
		pathlabel.config(text=self.filename)			##Filename is path to select the file
		pathlabel.grid(row=1,column=3,columnspan=3)
		self.master.protocol("WM_DELETE_WINDOW",lambda:self.on_exit(1))
	
	def on_exit(self,i):
			if(i==0):
				print("Sorry")
			else:
				self.master.destroy()

	
	def msg1(self):
		msg="Select the Course Data"
		w=Label(self.master,text=msg)
		w.grid(row=1, column=1,padx=20,pady=30) 

	def browseButton(self):
		self.browsebutton = Button(self.master, text="Browse", command=lambda:upexamdata.browsefunc(self))
		self.browsebutton.grid(row=1, column=2)

	def upload(self):
			if(self.uname!='' and self.pas!='' and self.dbname!=''):
				try:
					mydb = mysql.connector.connect( host="localhost",  user=self.uname, passwd=self.pas,database=self.dbname)
					if mydb.is_connected():
						cur = mydb.cursor(prepared=True)
	    			#cur = mydb.cursor(prepared=True)
						print("ok1"+self.filename)
						cur.execute("DROP TABLE IF EXISTS student_details;")
						cur.execute("CREATE TABLE student_details(Paper_Code int(20),Paper_year char(6),Course_code int(30),Year char(6),Semester char(6),Paper_name varchar(150),College_rollno varchar(60),University_rollno bigint(150),Name varchar(70))")
						book3=xlrd.open_workbook(self.filename)#excel2="course12 (1).xlsx"
						a=[] 
						b=[]
						c=[]
						i=0
						code_arr=[582,583,554,570,556,557,558,563,567,569,504]
						name1=["PS_details","LS_details","bms_details","CS_details","Botany_details","Chemistry_details","Electronics_details","Mathematics_details","Physics_details","Zoology_details","B.Com (H)_details"]
						for f in range(0,len(name1)):
							code_finder1= re.compile(r'(\d{8})') 
						
							sheet=book3.sheet_by_name(name1[f])
						
							for r in range(0,(sheet.nrows)):
								sql_insert_query3 = """ INSERT INTO student_details(Paper_code,Paper_year,Course_code,Year,Semester,Paper_name,College_rollno,University_rollno,Name) VALUES (%s,%s,%s, %s, %s, %s, %s, %s, %s)"""
						
							
								if code_finder1.search(str(sheet.cell(r,0).value)):
								
									a.append(sheet.cell(r,0).value)
							
									b.append(sheet.cell(r,1).value)
									
									c.append(sheet.cell(r,2).value)
									i=i+1
							
								elif sheet.cell(r,0).value=="SRNO":
								
									y=2
							
								elif len(str(sheet.cell(r,0).value))==0:
									while(i>=0):
										if a and b:
											a.pop()
											b.pop()
											c.pop()
											i=i-1
										else:
											break
									i=0
								
								else:
									for i in range(0,len(a)):
										univ=sheet.cell(r,2).value
						
										coll=sheet.cell(r,3).value 
						
										yr=sheet.cell(r,6).value

										sem=sheet.cell(r,7).value
						
										name=sheet.cell(r,8).value 
							
										insert_tuple_4=(a[i],c[i],code_arr[f],yr,sem,b[i],coll,univ,name)
								
										cur.execute(sql_insert_query3, insert_tuple_4)
							
										mydb.commit()
							
							
										print("Data inserted for ",name1[f] ,"table using the prepared statement")
						
				except mysql.connector.Error as error:
    
					print("parameterized query failed {}".format(error))
					
				finally:
					
					if (mydb.is_connected()):
						
						cur.close()
						
						mydb.close()
						
						print("MySQL connection is closed")


	def submit(self):
		sbt=Button(self.master,text="Submit",command=lambda:upexamdata.strt(self))
		sbt.grid(row=2, column =2)
		sbt1=Button(self.master,text="Close",command=lambda:self.master.destroy())
		sbt1.grid(row=2, column=1)
		
	def strt(self):
		if(upexamdata.i!=0):
			self.upload()
			self.master.destroy()
			#self.browsebutton["state"]="disabled"
#	   	  start database():

#	def databased(self): 				
		
		


#obj1=upexamdata()
#mainloop()

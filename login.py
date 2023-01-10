from tkinter import *
from tkinter import messagebox
import mysql.connector
import sys
import os

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')
							
class login(Frame):
	
	def __init__(self,master=None):
		super().__init__(master)
		self.design()
		self.grid()
		self.msg1()		
		self.msg2()
		self.msg3()
		self.uname='a'
		self.pas='b'
		self.dbname='c'
		self.passentry()
		self.dbentry()
		self.submit()
		self.label2()
		#self.path()
		

	def design(self):
		self.master.geometry('1000x700')
		self.master.title("SQL Login")
		self.master.grid_rowconfigure(0, weight=1)
		self.master.grid_rowconfigure(1, weight=1)
		self.master.grid_rowconfigure(2, weight=1)
		self.master.grid_rowconfigure(3, weight=1)
		self.master.grid_rowconfigure(4, weight=1)
		self.master.grid_rowconfigure(5, weight=1)
		self.master.grid_rowconfigure(6, weight=1)
		self.master.grid_columnconfigure(0, weight=1)
		self.master.grid_columnconfigure(3, weight=1)

	def msg1(self):
		msg="Username: "
		w=Label(self.master,text=msg)
		w.grid(row=1, column=1)
		self.e1 = Entry(self.master)		
		self.e1.grid(row=1, column=2)


	
	def msg2(self):
		msg="Password:"
		w=Label(self.master,text=msg)
		w.grid(row=2, column=1)

	def label2(self):
		label = Label( self.master, text = "SQL LOGIN")
		label.place(relx = 0.5, rely = 0.05, anchor = 'n')

	def passentry(self):
		self.e2 = Entry(self.master,show="*")		
		self.e2.grid(row=2, column=2)
					

	def msg3(self):
		msg="Database Name:"
		w=Label(self.master,text=msg)
		w.grid(row=3,column=1)

	def dbentry(self):
		self.e3 = Entry(self.master)
		self.e3.grid(row=3, column=2)
	




	def submit(self):
		
		sbt=Button(self.master,text="Submit",command=lambda:login.strt(self))
		sbt.grid(row=5, column=2)
	
	def strt(self):
		
		self.uname=self.e1.get()
		self.pas=self.e2.get()
		self.dbname=self.e3.get()
		if(self.uname!='' and self.pas!='' and self.dbname!=''):
			try:
				mydb = mysql.connector.connect( host="localhost",  user=self.uname, passwd=self.pas,database=self.dbname)
				if mydb.is_connected():
		    		#cur = mydb.cursor(prepared=True)
					print("db displayed sucessfully")
					self.master.destroy()
					root.update()
				else:
					print("error while connecting to database")
			except:
				print("Wrong Credentials")
			
		else:
			print("Empty")
			

root=Tk()
'''o=login(root)
mainloop()
print(o.uname)	
	'''
class A(Frame):
	def __init__(self,master=None):
		super().__init__(master)
		self.getpass()
		self.print()
		
	def getpass(self):
		rt=Toplevel()
		o=login(rt)
		rt.mainloop()
		print(o.uname,o.pas,o.dbname)

	def print(self):
		self.master.update()
		print("dsasd")
               	    
o=A(root)	
mainloop
		




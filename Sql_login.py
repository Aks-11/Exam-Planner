from tkinter import *
import mysql.connector
import generate
							
class login(Frame):
	
	def __init__(self,master=None):
		super().__init__(master)
		self.design()
		self.grid()
		self.msg1()		
		self.msg2()
		self.msg3()
		self.msg4()
		self.msg5()
		self.tinfo()
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
	
	def msg4(self):
		msg="How many Student invigilated by one teacher"
		w=Label(self.master,text=msg)
		#w.config(width=300)
		w.grid(row=4,column=1,pady=20, sticky=W)
	
		msg2="Minimum number of extra teacher per day"
		x=Label(self.master,text=msg2)
		
		x.grid(row=5,column=1,pady=30, sticky=W)

	def tinfo(self):
		self.e4=Spinbox(self.master, from_ = 0, to = 100)
		self.e4.grid(row=4,column=3,sticky=W)
		self.e5=Spinbox(self.master, from_ = 0, to = 100)
		self.e5.grid(row=5,column=3,sticky=W)

	def msg5(self):
		msg="Enter Directory name to be created "
		w=Label(self.master,text=msg)
		w.grid(row=6, column=1)
		self.e6 = Entry(self.master)		
		self.e6.grid(row=6, column=2)


	def submit(self):
		
		sbt=Button(self.master,text="Submit",command=lambda:login.strt(self))
		sbt.grid(row=7, column=2)
	
	def strt(self):
		
		uname=self.e1.get()
		pas=self.e2.get()
		dbname=self.e3.get()
		i1=self.e4.get()
		i2=self.e5.get()
		i3=self.e6.get()
		
		if(uname!='' and pas!='' and dbname!='' and i1!=0 and i2!=0 and i3!=0):
			
		#	try:
			mydb = mysql.connector.connect( host="localhost",  user=uname, passwd=pas,database=dbname)
			if mydb.is_connected():
				r=generate.generate(uname,pas,dbname,i1,i2,i3,self.master)
				#cur = mydb.cursor(prepared=True)
				print("db displayed sucessfully")
				self.master.destroy()
				if (r==0):
					messagebox.showinfo("Message Box","Directory successfully generated") 
					self.master.destroy() 
				elif(r==1):
					messagebox.showinfo("Error","Folder already exist")
				else:
					messagebox.showinfo("Error", "Error1") 
			else:
				messagebox.showinfo("error while connecting to database")
			'''except :
				p = sys.exc_info()[0]
				print(p)
				messagebox.showinfo("Message Box","Error2 ")'''

		else:
			messagebox.showinfo("Message Box","Enter Details")
			 	
			
                	    
 				
		
		




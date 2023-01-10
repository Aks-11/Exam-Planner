from tkinter import *
from tkinter import messagebox
import mysql.connector


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
					rt=Toplevel()
					Exam_committee(self.uname,self.pas,self.dbname,rt)
					rt.mainloop()
				else:
					messagebox.showinfo("error while connecting to database")
			except:
				messagebox.showinfo("Message Box","Error ")
		else:
			messagebox.showinfo("Message Box","Enter Details")


#master = Tk()
class Exam_committee(Frame):
	def __init__(self,user,key,db,master=None):
		super().__init__(master)
		self.master.geometry('300x600')
		self.uname=user
		self.pas=key
		self.dbname=db
		self.myresult=[] 
		self.database()
		self.q={}
		self.design()
		
		
		#self.chkbutton()
		#self.button()
		

	def database(self):
		mydb = mysql.connector.connect( host="localhost",  user=self.uname, passwd=self.pas,database=self.dbname)
		if mydb.is_connected():
		      cur = mydb.cursor(prepared=True)
		      print("db displayed sucessfully")
		else:
			print("error while connecting to database")
		cur=mydb.cursor()
		cur.execute("select Name, availibility from teachers")
		self.myresult= cur.fetchall()
		
	def design(self):	
		scrollbar = Scrollbar(self.master) 
		self.w = Canvas(self.master, width=40, height=60,yscrollcommand=scrollbar.set) 
			
		canvas_height=20
		canvas_width=200
		scrollbar.config(command=self.w.yview)
	
		scrollbar.pack( side = RIGHT, fill = Y)
	
		self.w.config(scrollregion=(0,0,0,20))
		self.f=Frame(self.w)
		
		self.w.pack(side="left", fill="both", expand=True)       #Updated the window creation
		self.w.create_window(0,0,window=self.f, anchor='nw')
		x=0
		y=0
	#states=[]
		
		Exam_committee.msg(self)
		Exam_committee.chkbutton(self)
		Exam_committee.button(self)
	
	def msg(self):
		lbl=Label(self.f,text="Select Members of Exam Committee ")
		lbl.pack()
		
	def chkbutton(self):

		for name,avail in self.myresult:
			if(avail=='S'):
				#print(type(name))
				var=IntVar()
				chk = Checkbutton(self.f, text=str(name), variable=var,offvalue=-1)
				chk.pack(side=BOTTOM,anchor=W)	#states.append(var)			
				chk.select()
				self.q[name]=var
			else:
				#print(type(name))
				var=IntVar()
				chk = Checkbutton(self.f, text=str(name), variable=var)
				chk.pack(side=BOTTOM,anchor=W)	#states.append(var)			
				self.q[name]=var
				
		

	def run(self):	
		#print(list(map((lambda var: var.get()),states)))
		S=''
		for key in self.q:
			if((self.q[key]).get()==1):
				S=S+'\n'+key
				
		

		if messagebox.askokcancel("Name of member of Exam Committee",S,default="cancel"):
			for k in self.q:
				self.q[k]=(self.q[k]).get()
			self.sql()	
			self.master.destroy()
		
	def button(self):
		Button(self.f,text="Close", command =self.master.destroy).pack(side=LEFT)
		Button(self.f,text="Submit", command =lambda:self.run()).pack(side=LEFT)
		self.master.update()
		self.w.config(scrollregion=self.w.bbox("all"))
		
	#l=list(map((lambda var: var.get()),states))
	
	def sql(self):
		mydb = mysql.connector.connect( host="localhost",  user=self.uname, passwd=self.pas,database=self.dbname)
		if mydb.is_connected():
			cur = mydb.cursor(prepared=True)
			
			for key in self.q:
				if(self.q[key]==1):
					sql_insert_query1 = "update teachers set availibility='S' where Name=%s"
					cur.execute(sql_insert_query1, (key,))
				if(self.q[key]==-1):
					sql_insert_query1 = "update teachers set availibility='I' where Name=%s"
					cur.execute(sql_insert_query1,(key,))
			mydb.commit()
		else:
			print("error while connecting to database")
#obj1=Exam_committee(master)	
#mainloop() 


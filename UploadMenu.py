from tkinter import *
from Datesheet import *
from Teacher_list import *
from Exam_data import *
from Room_list import *
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
				mydb1 = mysql.connector.connect(host="localhost",user=self.uname,password=self.pas)

				mycursor = mydb1.cursor()

				mycursor.execute("SHOW DATABASES")
			
				flag=0
				for x in mycursor:
					if(self.dbname in x):
						flag=1
				
				if flag==1:
				
					mydb1.close()
					mydb = mysql.connector.connect( host="localhost",  user=self.uname, passwd=self.pas,database=self.dbname)
					
					if mydb.is_connected():
					#cur = mydb.cursor(prepared=True)
						print("db displayed sucessfully")
						self.master.destroy()
						rt=Toplevel()
						uploadwindow(self.uname,self.pas,self.dbname,rt)
						rt.mainloop()
					else:
						messagebox.showinfo("error while connecting to database")
				
				if flag==0:
					if messagebox.askokcancel("Database Name does not exist","Create Database",default="cancel"):
						mycursor.execute("CREATE DATABASE %s" %self.dbname)
						mydb1.close()
						mydb = mysql.connector.connect( host="localhost",  user=self.uname, passwd=self.pas,database=self.dbname)
						if mydb.is_connected():
						#cur = mydb.cursor(prepared=True)
							print("db displayed sucessfully")
							self.master.destroy()
							rt=Toplevel()
							uploadwindow(self.uname,self.pas,self.dbname,rt)
							rt.mainloop()
						else:
							messagebox.showinfo("error while connecting to database")
			except:
				messagebox.showinfo("Message Box","Error ")
		else:
			messagebox.showinfo("Message Box","Enter Details")


class CreateToolTip(object):
	'''create a tooltip for a given widget'''	
	def __init__(self, widget, text='widget info',master=None):
		self.master=master
		self.design()
		self.widget = widget
		self.text = text
		self.widget.bind("<Enter>", self.enter)
		self.widget.bind("<Leave>", self.close)
	    
	def design(self):
		self.master.geometry("1000x400")
		self.master.title("Upload Menu")
		self.master.grid_rowconfigure(0, weight=1)
		self.master.grid_columnconfigure(0, weight=1)
		self.master.grid_columnconfigure(5, weight=1)
			
	def enter(self, event=None):
	        x = y = 0
	        x, y, cx, cy = self.widget.bbox("insert")
	        x += self.widget.winfo_rootx() + 25
	        y += self.widget.winfo_rooty() + 20
	        # creates a toplevel window
	        self.tw = Toplevel(self.widget)
	        # Leaves only the label and removes the app window
	        self.tw.wm_overrideredirect(True)
	        self.tw.wm_geometry("+%d+%d" % (x, y))
	        label = Label(self.tw, text=self.text, justify='left',
	                       background='light blue', relief='solid', borderwidth=1,
	                       font=("times", "10", "normal"))
	        label.pack(ipadx=1)
	def close(self, event=None):
        	if self.tw:
        	    self.tw.destroy()
	
		
class uploadwindow(Frame):
        
	def __init__(self,user,key,db,master=None):
		super().__init__(master)
		self.grid()
		self.uname=user
		self.pas=key
		self.dbname=db
		self.Upload_Datesheet_Buttton()
		self.Upload_ExamData_Buttton()
		self.Upload_RoomCapacity_Buttton()
		self.Upload_TeacherList_Buttton()
		self.label1()
		self.submit()
		
		
	'''def on_exit(self,i):
			if(i==0):
				print("Sorry")
				
			else:
				self.master.destroy()'''
	def label1(self):
		label = Label( self.master, text = "UPLOAD EXCEL (.xls) FILES ONLY")
		label.place(relx = 0.5, rely = 0.25, anchor = 'n')
	
	def Datesheet(self):		
		print("Datesheet Upload")
		rt=Toplevel()
		rt.grab_set()
		self.i=updatesheet(self.uname,self.pas,self.dbname,rt)
		rt.mainloop()
		
		
		
        
	def Exam(self):
		print("Course Data Upload")
		rt=Toplevel()
		rt.grab_set()
		obj2=upexamdata(self.uname,self.pas,self.dbname,rt)
		rt.mainloop()

	def Room(self):
		print("Room Capacity Upload")
		rt=Toplevel()
		rt.grab_set()
		obj3=uproomlist(self.uname,self.pas,self.dbname,rt)
		rt.mainloop()

                        
	def TeacherList(self):

		print("Teacher List Upload")
		rt=Toplevel()
		rt.grab_set()
		obj4=uptlist(self.uname,self.pas,self.dbname,rt)
		rt.mainloop()


	def Upload_Datesheet_Buttton(self):
		B1 =Button(self.master,text =" Datesheet ", command =self.Datesheet)
		B1.grid(row=0,column=1,padx=30, pady=30, sticky="")
		button1_ttp = CreateToolTip(B1, "Upload the converted \ndatesheet file",self.master)
                
	def Upload_ExamData_Buttton(self):
		B2 =Button(self.master,text =" Course Data ", command = self.Exam)
		B2.grid(row=0,column=2,padx=30,pady=30, sticky="")
		button2_ttp = CreateToolTip(B2, "Upload the Exam Data file\n which contains exam details\n of respective courses along \n with student details at the \nbottom",self.master)

	def Upload_RoomCapacity_Buttton(self):
		B3 =Button(self.master, text =" Room Capacity ", command = self.Room)
		B3.grid(row=0,column=3,padx=30,pady=30, sticky="")
		button3_ttp = CreateToolTip(B3, "Upload the file containing \nroom capacity details",self.master)

	def Upload_TeacherList_Buttton(self):
		B4 =Button(self.master,text =" Teacher List ", command = self.TeacherList)
		B4.grid(row=0,column=4,padx=30,pady=30, sticky="")
		button4_ttp = CreateToolTip(B4, "Upload the file with details\n of teachers for examination duties",self.master)

	def submit(self):
		subt=Button(self.master,text="Submit",command=self.end)
		subt.grid(row=1,column=2,padx=30,pady=30, sticky="")

		sbt1=Button(self.master,text="Close",command=lambda:self.master.destroy())
		sbt1.grid(row=1, column=3)

	def end(self):
		print('END')
		self.master.destroy()    

#root =Tk()


#ob1=uploadwindow(root)
#mainloop()

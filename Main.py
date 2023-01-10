
from tkinter import *
import UploadMenu as um
import Teacher_on_leave as tol 
import Exam_committee as ec
import Sql_login
import sys
import os

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')
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
		self.master.title("Main Menu")
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
	
		
class mainwindow(Frame):
        
	def __init__(self,master=None):
		super().__init__(master)
		self.grid()
		self.Upload_Buttton()
		self.Teacher_on_leave_Buttton()
		self.Exam_committee_Buttton()
		self.Arrangement_Buttton()
		self.label1()

	
	def label1(self):
		label = Label( root, text = "Welcome")
		label.place(relx = 0.5, rely = 0.25, anchor = 'n')
	
	def Upload(self):
		rt=Toplevel()
		rt.grab_set()
		obj1=um.login(rt)
		rt.mainloop()
		
        
	def Teacher_on_leave(self):
		rt=Toplevel()
		rt.grab_set()
		obj1=tol.login(rt)
		rt.mainloop()

	def Exam_committee(self):
		rt=Toplevel()
		rt.grab_set()
		obj1=ec.login(rt)
		rt.mainloop()

                        
	def Arrangement(self):
		rt=Toplevel()
		rt.grab_set()
		obj1=Sql_login.login(rt)
		rt.mainloop()

	def Upload_Buttton(self):
		B1 =Button(self.master,text =" Upload Database ", command =self.Upload)
		B1.grid(row=0,column=1,padx=30, pady=30, sticky="")
		button1_ttp = CreateToolTip(B1, "Upload datesheet, Teacher list,\n room list ,Exam data",self.master)

	def Exam_committee_Buttton(self):
		B3 =Button(self.master, text =" Exam_committee", command = self.Exam_committee)
		B3.grid(row=0,column=2,padx=30,pady=30, sticky="")
		button3_ttp = CreateToolTip(B3, "Select member of exam committee",self.master)

                
	def Teacher_on_leave_Buttton(self):
		B2 =Button(self.master,text =" Teacher_on_Leave ", command = self.Teacher_on_leave)
		B2.grid(row=0,column=3,padx=30,pady=30, sticky="")
		button2_ttp = CreateToolTip(B2, "Select Teacher who are on leave",self.master)

	
	def Arrangement_Buttton(self):
		B4 =Button(self.master,text =" Arrangement ", command = self.Arrangement)
		B4.grid(row=0,column=4,padx=30,pady=30, sticky="")
		button4_ttp = CreateToolTip(B4, "Get Siting Arrangement \nand teacher schedule",self.master)
    

root =Tk()


ob1=mainwindow(root)
mainloop()

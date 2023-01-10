#!/usr/bin/env python
# coding: utf-8

# In[5]:


import mysql.connector as ms
import pandas as pd 
import numpy as np
import math
from tkinter import *
from tkinter import filedialog
import os
import xlsxwriter
import shutil
from collections import namedtuple
from mysql.connector import Error
def generate(username,dbpass,dbname,techr_pr_students,extra,dr,master):
    
    directory = dr
    data_path = [('All tyes(*.*)', '*.*')]
  

   
    # Parent Directory path 
    parent_dir =filedialog.askdirectory(parent=master) + "/"  #changes


    # Path 
    path = os.path.join(parent_dir,directory) 

    # Create the dir2019-05-24ectory 
    # 'GeeksForGeeks' in 
    # '/home / User / Documents' 
    isdir = os.path.isdir(path)  
    if(isdir):
        return 1;
    else:
        os.mkdir(path)

        
    #finding total duties for invigilator
    def i_duty(query , arr , extra): 
        sum =0
        connect_data = pd.read_sql_query(query, mydb)
        connect= connect_data.sum()
        num= int(connect)
        arr.append(num)
        sum =  math.ceil(num/tps)
        if(sum > 0): #for days their is no exam specially for evening
            return sum+extra; # two extra teachers
        else :
            return 0;





    # finding duties for supervisors
    def s_duty(query):
        connect_data = pd.read_sql_query(query, mydb)
        connect= connect_data.sum()
        num= int(connect)
        if(num >0 and num<= 150):
            return 1;
        elif(num>150 and num<=300):
            return 2;
        elif(num>300):
            return 3;
        else:
            return 0;



    
    #connecting database with python
    mydb = ms.connect(
        host = 'localhost',
        user = username,
        password = dbpass, #changes
        database = dbname#changes
        )

    # reading the distinct dates of exams and storing it too array
    data = pd.read_sql_query("SELECT DISTINCT(Date) FROM course order by Date ",mydb)
    date= pd.DataFrame(data["Date"])
    date_arr= date.to_numpy(dtype = 'str')

     # taking no of students for which one teacher is required
    tps= int(techr_pr_students)
    etc= int(extra)
    # taking exam names and sum of students per day
    sql='SELECT sum(sum) from course where Date ='# joining tables to get the sum

    #taking variables for sum of students as sum_m for morning student sum and sum_e for evening student
    sum_m=0
    sum_e=0

    supr_d=0

    mor_arr= [];
    eve_arr=[];
    exam_date =[];
    for sql1 in date_arr:# taking all the dates one by one and taking sum of students attending the exam per day
        a=sql.join(sql1)
        exam_date.append(a)
        query1 = sql+"'"+a+"'and session = 'MORNING'"# for morning session
        query2 = sql+"'"+a+"' and session = 'EVENING'"# for evening session
        sum_m +=i_duty(query1,mor_arr,etc)
        sum_e +=i_duty(query2, eve_arr,etc)
        supr_d = supr_d + s_duty(query1) + s_duty(query2)


    invigi_d=sum_m + sum_e        #total no of duties given to teachers
    #print("Total duties of invigilator",invigi_d)
    #print("Total duties of supervisors",supr_d)


    list_of_tuples = list(zip(exam_date, mor_arr,eve_arr))  
    df = pd.DataFrame(list_of_tuples, columns = ['Date', 'Morning_student', 'Evening Student'])



    #finding count of invigilators and supervisors
    i_data =  pd.read_sql_query("SELECT tid from teachers where availibility ='I' ",mydb)
    i_count = len(i_data.index)
    #print("No. of invigailators available",i_count)

    s_data =  pd.read_sql_query("SELECT tid from teachers where availibility ='S' ",mydb)
    s_count = len(s_data.index)
    #print("No of supervisors available",s_count)







    #finding the upper bound of duties
    x= invigi_d/i_count
    y= math.trunc(x)
    z=x-y
    if(z==0):
        min_duty_i = x+1
    else:
        min_duty_i = math.ceil(x)
    min_duty_s = math.ceil(supr_d/s_count)
    #print("min duties to be done by each invigilator",min_duty_i)
    #print("min duties to be done by each supervisor",min_duty_s)
    #print(df)

    # storing room data into object for further use
    class myroom(object):
        def __init__(self,roomno):
            self.no= roomno
            self.capacity=0;
            self.columns= 0;
            self.total_rows= 0;

            room= pd.read_sql_query("SELECT * from  room_data",mydb);
            value = room[room['RNo'] == roomno];


            self.capacity = int( value['Capacity'].to_numpy(dtype = 'int'));

            self.columns=   int( value['Row'].to_numpy(dtype = 'int'));

            self.total_rows= int(self.capacity/2);   
    my_room_objects=[];


    room=  pd.read_sql_query("SELECT * from  room_data",mydb)
    rom= pd.DataFrame(room["RNo"])
    rom_arr=  rom.to_numpy(dtype = 'int')
    room_arr = [];
    ##print(room)
    for i in rom_arr:
        room_arr.append(int(i));

    for i in room_arr:
        my_room_objects.append(myroom(i));

    #for obj in my_room_objects:
        ##print (obj.no, obj.capacity,obj.columns,obj.total_rows) #printing details of rooms



    class MyClass(object):
        def Repeat(x): 
            _size = len(x) 
            repeated = [] 
            for i in range(_size): 
                k = i + 1
                for j in range(k, _size): 
                    if x[i] == x[j] and x[i] not in repeated: 
                        repeated.append(x[i]) 
            return repeated 


        def __init__(self, date, session):
            self.date = date
            self.session= session
            self.papercode=[];
            self.total=[];
            self.course=[];
            self.year = [];
            self.room_used=[];
            self.room_strength=[];
            self.a=0;
            self.b=0;
            self.a_arr=[];
            self.b_arr=[];
            self.a_course=[];
            self.b_course=[];
            self.a_year=[];
            self.b_year=[];
           # #print(self.date)



            # for morning session
            #creating array of papers on that day

            data= pd.read_sql_query("select Paper_Code,sum, Course_Code, Year from course where Date = '"+date+"' and session ='"+session+"'", mydb)
            data1= pd.DataFrame(data["Paper_Code"])
            data_arr= data1.to_numpy(dtype = 'int')
            papercode_arr = [];
            for i in data_arr:
                papercode_arr.append(int(i))

            ##print (papercode_arr)
            data1= pd.DataFrame(data["sum"])
            data_arr= data1.to_numpy(dtype = 'int')
            total_arr = [];
            for i in data_arr:
                total_arr.append(int(i))

            data1= pd.DataFrame(data["Course_Code"])
            data_arr= data1.to_numpy(dtype = 'int')
            Course_Code = [];
            for i in data_arr:
                Course_Code.append(int(i))
            data1= pd.DataFrame(data["Year"])
            data_arr= data1.to_numpy(dtype = 'str')
            year_n = [];
            for i in data_arr:
                year_n.append(i)
            ##print(year_n,"year")
            year=[]
            for x in year_n:
                a=sql.join(x)
                year.append(a)
            # #print (total_arr)
           # #print(data)

            index_arr = np.argsort(total_arr) 
            desc_index_arr= index_arr[::-1] 



            for i in desc_index_arr:
                self.papercode.append(papercode_arr[i])
                self.total.append(total_arr[i])
                self.course.append(Course_Code[i])
                self.year.append(year[i])



            #finding same papercode on particular date or same type of exam
            duplicate = MyClass.Repeat(self.papercode)
            ##print(duplicate,"duplicate")
            a=0;
            b=0;
            for m in range(len(duplicate)):
                if(a<=b):
                    for i in range(len(self.papercode)):
                        if(self.papercode[i] == duplicate[m]):
                            a+= self.total[i]
                            self.a_arr.append(self.papercode[i])
                            self.a_course.append(self.course[i])
                            self.a_year.append(self.year[i])

                else:
                    for i in range(len(self.papercode)):
                        if(self.papercode[i] == duplicate[m]):
                            b+= self.total[i]
                            self.b_arr.append(self.papercode[i])
                            self.b_course.append(self.course[i])
                            self.b_year.append(self.year[i])


            help1=[];
            help2=[];
            help3=[];
            help4=[];
            for j in range(len(self.papercode)):
                if self.papercode[j] not in duplicate:
                    help1.append(self.papercode[j])
                    help2.append(self.total[j])
                    help3.append(self.course[j])
                    help4.append(self.year[j])


            ##print(help1)
            ##print(help2)
            ##print(help3)
            ##print(help4)
            self.papercode=help1;             
            self.total=help2;
            self.course=help3;
            self.year=help4;




            #setting arrangement in a and b

            if(len(self.total)>0):
                if(a==0):
                    a+=self.total[0];
                    self.a_arr.append(self.papercode[0])
                    self.a_course.append(self.course[0])
                    self.a_year.append(self.year[0])
                  #  #print(len(self.total))
                    for i in range(1 , len(self.total)):
                       # #print(i,"i")
                        if(a>b):
                            b= b+ self.total[i]
                            self.b_arr.append(self.papercode[i])
                            self.b_course.append(self.course[i])
                            self.b_year.append(self.year[i])
                        #    #print("ello")
                        else :
                            a= a+self.total[i]
                            self.a_arr.append(self.papercode[i])
                            self.a_course.append(self.course[i])
                            self.a_year.append(self.year[i])
                         #   #print("ello")
                else:
                    for i in range(0 , len(self.total)):
                       # #print(i,"i")
                        if(a>b):
                            b= b+ self.total[i]
                            self.b_arr.append(self.papercode[i])
                            self.b_course.append(self.course[i])
                            self.b_year.append(self.year[i])
                        #    #print("ello")
                        else :
                            a= a+self.total[i]
                            self.a_arr.append(self.papercode[i])
                            self.a_course.append(self.course[i])
                            self.a_year.append(self.year[i])
                         #   #print("ello")

            req_rows=0;
            used_room_obj=[];
            self.a=a;
            self.b=b;
            ##print(a,"a")
            ##print(b,"b")    
            #taking the maximum no of rows required in the exam used further to find total no of rooms
            if(a>b):
                req_rows=a;

            else:
                req_rows=b;


            rows_room=0;
                #storing the no of rooms to be used in the exam in self.room_used and object of used rooms in used_room_obj
            for rno in my_room_objects:
                if(rows_room < req_rows):
                    rows_room += (rno.total_rows);
                    self.room_used.append(rno.no)
                    used_room_obj.append(rno)
                else:
                    break;


                # storing the strength of students in a room in self.room_strength array
            for value in used_room_obj:
                    if(a>= value.total_rows and b>=value.total_rows):
                        a= a- value.total_rows;
                        b= b- value.total_rows;
                       # #print(value.capacity)
                        saved= value.capacity
                        self.room_strength.append(saved)
                        ##print(saved,"capacity")
                    elif(a>= value.total_rows and b< value.total_rows):
                        a=a- value.total_rows;
                        ##print(value.total_rows+b)
                        saved= value.total_rows + b
                        self.room_strength.append(saved)
                        b=0;
                        ##print(saved,"capacity")
                    elif(b>= value.total_rows and a< value.total_rows):
                        b=b-value.total_rows;
                        saved = value.total_rows + a;
                        self.room_strength.append(saved)
                        a=0;
                        ##print(saved,"capacity")
                    else:
                        saved=a+b
                        self.room_strength.append(saved)
                        a=0;
                        b=0;
                        ##print(saved,"capacity")


           # #print(self.papercode)
            ##print(self.total)
            self.papercode=[]
            self.total=[]
            self.course=[]
            self.year=[];
            for new in desc_index_arr:
                self.papercode.append(papercode_arr[new])
                self.total.append(total_arr[new])
                self.course.append(Course_Code[new])
                self.year.append(year[new])   

    my_objects = []

    for i in exam_date:
        my_objects.append(MyClass(i,'MORNING'))
        my_objects.append(MyClass(i,'EVENING'))
    #for obj in my_objects:
        ##print (obj.date,"Exam date")
        ##print (obj.session,"session")
        ##print (obj.papercode, "papercode of papers")
        ##print (obj.course , "course")
        ##print (obj.total, "sum of students")
        ##print (obj.room_used,"room used")
        ##print (obj.room_strength ,"strength")
        ##print (obj.a)
        ##print (obj.b)
        ##print (obj.a_arr)
        ##print (obj.b_arr)
        ##print (obj.a_course)
        ##print (obj.b_course)
        ##print (obj.a_year)
        ##print (obj.b_year) 


    #print("check")
    #code by harsh putting duties
    #***********************variable declaration*************
    name_p=[]
    sum=0
    x=[]
    ex=0
    name_t=[]
    name_s=[]
    count_p=[]
    department_s=[]

    count_t=[]
    status_p=[]
    status_t=[]
    department_p=[]
    department_t=[]
    extra_teacher=[]
    extra_sup=[]

    #**************Creating daily requirement array for supervisors*********
    for su  in range(0,len(exam_date)):
        if mor_arr[su]==0:
            extra_sup.append(0)
        if mor_arr[su]>0 and mor_arr[su]<=150:
            extra_sup.append(1)
        if mor_arr[su]>150 and mor_arr[su]<=300:
            extra_sup.append(2)
        if mor_arr[su]>300:
            extra_sup.append(3)
        if eve_arr[su]==0:
            extra_sup.append(0)
        if eve_arr[su]>0 and eve_arr[su]<=150:
            extra_sup.append(1)
        if eve_arr[su]>150 and eve_arr[su]<=300:
            extra_sup.append(2)
        if eve_arr[su]>300:
            extra_sup.append(3)
    #**************CREATING DAILY REQUIREMENT ARRAY FOR TEACHERS********
    for iii in range(0,len(exam_date)):
        if mor_arr[iii]==0:
            extra_teacher.append(0)
        if(mor_arr[iii]>0 and mor_arr[iii]<300):
            extra_teacher.append(3)
        if mor_arr[iii]>=300 and mor_arr[iii]<600:
            extra_teacher.append(4)
        if mor_arr[iii]>=600 and mor_arr[iii]<900:
            extra_teacher.append(5)
        if mor_arr[iii]>=900:
            extra_teacher.append(6)
        if eve_arr[iii]==0:
            extra_teacher.append(0)
        if(eve_arr[iii]>0 and eve_arr[iii]<300):
            extra_teacher.append(3)     
        if(eve_arr[iii]>=300 and eve_arr[iii]<600):
            extra_teacher.append(4)
        if eve_arr[iii]>=600 and eve_arr[iii]<900:
            extra_teacher.append(5) 
        if eve_arr[iii]>=900:
            extra_teacher.append(6)

    if mydb.is_connected():
        cur = mydb.cursor(prepared=True)
        #print("db displayed sucessfully")
    else:
        print("error while connecting to database")
    #***********FETCHING DATA FROM TEACHERS TABLE STORINF IN ARRAY*****
    #print("check2")
    cur=mydb.cursor()
    cur.execute("Select * from teachers;")
    records=cur.fetchall()
    
    for row in records:
        if row[5]=="Permanent" and row[6]=="I":
            name_p.append(row[1])
            department_p.append(row[4])
            status_p.append(row[5])
            count_p.append(5)
        elif row[5]=="Adhoc" and row[6]=="I":
            name_t.append(row[1])
            department_t.append(row[4])
            status_t.append(row[5])
            count_t.append(5)
        elif row[6]=="S":
            name_s.append(row[1])
            department_s.append(row[4])
    
    cur.execute("DROP TABLE IF EXISTS mysamp;")
    #print("check4")
    cur.execute("CREATE TABLE mysamp(Name varchar(50),Department varchar(20),room varchar(10),date varchar(50),session varchar(10),status char(10));")
    #print("check1")
    #**********LINKED LIST CLASS**********
    class Node:
        def __init__(self, data,department,count):
                self.data = data 
                self.department=department
                self.count=count
                self.next = None


    class CircularLinkedList:
        def __init__(self):
            self.head = None 


        def append(self, data,department,count):
            if not self.head:
                self.head = Node(data,department,count)
                self.head.next = self.head
            else:
                new_node = Node(data,department,count)
                cur = self.head
                while cur.next != self.head:
                    cur = cur.next
                cur.next = new_node
                new_node.next = self.head

    #**********PRINTING LINKED LIST***********
        def print_list(self):
            cur = self.head 

            while cur:
                #print(cur.data,cur.department,cur.count)
                cur = cur.next
                if cur == self.head:
                    break

    #***********FUNCTION FOR SUPERVISORS************
        def newlist1(self,list3):
            cur3=list3
            ww=0
            for j in my_objects:
                days1=j.date
                e1=j.session
                sup=extra_sup[ww]
                ww=ww+1
                #print("done")
                check1=0
                while(1):
                    if sup!=0:
                        sql_insert_query4 = """ INSERT INTO mysamp(Name,Department,room,date,session,status) VALUES (%s, %s, %s, %s, %s,%s)"""
                        a=cur3.data
                        b=cur3.department
                        c="NULL"
                        d=days1
                        f="Supervisor"
                        insert_tuple_5 = (a,b,c,d,e1,f)
                        cur.execute(sql_insert_query4, insert_tuple_5)
                        mydb.commit()
                        cur3.count=cur3.count+1
                        cur3=cur3.next
                        check1+=1
                        #print("insert done")
                        if(check1==sup):
                            break;
                    else:
                        break
    #***************FUNCTION FOR TEACHERS*******************  
        def newlist(self,list1,list2):
            cur1=list1
            cur2=list2
            w=0
            for j in my_objects:
                room= j.room_used;
                ssir=j.room_strength;
                days= j.date;
                e=j.session;
                ext=extra_teacher[w]
                w=w+1
                #print(ext)
                #print("done")
                check=0        
                while(len(room)>0):
                    if ext!=0:

                        if (cur1.count<min_duty_i+1):
                            sql_insert_query4 = """ INSERT INTO mysamp(Name,Department,room,date,session,status) VALUES (%s, %s, %s, %s, %s,%s)"""
                            a=cur1.data
                            b=cur1.department
                            c=0
                            d=days
                            f="P"
                            insert_tuple_5 = (a,b,c,d,e,f)
                            cur.execute(sql_insert_query4, insert_tuple_5)
                            mydb.commit()
                            cur1.count=cur1.count+1
                            cur1=cur1.next
                            check+=1
                            if(check==ext):
                                break;
                        if (cur2.count<min_duty_i+1):
                            sql_insert_query4 = """ INSERT INTO mysamp(Name,Department,room,date,session,status) VALUES (%s, %s, %s, %s, %s,%s)"""
                            a=cur2.data
                            b=cur2.department
                            c=0
                            d=days
                            f="T"
                            insert_tuple_5 = (a,b,c,d,e,f)
                            cur.execute(sql_insert_query4, insert_tuple_5)
                            mydb.commit()
                            cur2.count=cur2.count+1
                            cur2=cur2.next
                            check+=1
                            if(check==ext):
                                break;



                        elif(cur1.count>=min_duty_i and cur2.count<min_duty_i):
                            cur2= cur2.next

                        elif(cur1.count<min_duty_i and cur2.count>=min_duty_i):
                            cur1= cur1.next

                        else:
                            cur1= cur1.next
                            cur2= cur2.next
                    else:
                        break;

                for i in range(0,len(ssir)):
                    y=ssir[i]/18
                    x.append(round(y, 0))

                    if x[i]==1:
                        sql_insert_query4 = """ INSERT INTO mysamp(Name,Department,room,date,session,status) VALUES (%s, %s,%s, %s, %s, %s)"""
                        a=cur1.data
                        b=cur1.department
                        c=room[i]
                        d=days
                        f="P"
                        insert_tuple_5 = (a,b,c,d,e,f)
                        cur.execute(sql_insert_query4, insert_tuple_5)
                        mydb.commit()
                        cur1.count=cur1.count+1
                        cur1=cur1.next
                    if x[i]==2:

                        sql_insert_query4 = """ INSERT INTO mysamp(Name,Department,room,date,session,status) VALUES (%s,%s, %s, %s, %s, %s)"""
                        a=cur1.data
                        b=cur1.department
                        c=room[i]
                        d=days
                        f="P"
                        insert_tuple_5 = (a,b,c,d,e,f)
                        cur.execute(sql_insert_query4, insert_tuple_5)
                        mydb.commit()
                        cur1.count=cur1.count+1
                        cur1=cur1.next

                        sql_insert_query4 = """ INSERT INTO mysamp(Name,Department,room,date,session,status) VALUES (%s, %s,%s, %s, %s, %s)"""
                        a=cur2.data
                        b=cur2.department
                        c=room[i]
                        d=days
                        f="T"
                        insert_tuple_5 = (a,b,c,d,e,f)
                        cur.execute(sql_insert_query4, insert_tuple_5)
                        mydb.commit()
                        cur2.count=cur2.count+1
                        cur2=cur2.next

                    if x[i]==3:

                        sql_insert_query4 = """ INSERT INTO mysamp(Name,Department,room,date,session,status) VALUES (%s, %s, %s, %s, %s,%s)"""
                        a=cur1.data
                        b=cur1.department
                        c=room[i]
                        d=days
                        f="P"
                        insert_tuple_5 = (a,b,c,d,e,f)
                        cur.execute(sql_insert_query4, insert_tuple_5)
                        mydb.commit()
                        cur1.count=cur1.count+1
                        cur1=cur1.next

                        sql_insert_query4 = """ INSERT INTO mysamp(Name,Department,room,date,session,status) VALUES (%s, %s, %s, %s, %s,%s)"""
                        a=cur1.data
                        b=cur1.department
                        c=room[i]
                        d=days
                        f="P"
                        insert_tuple_5 = (a,b,c,d,e,f)
                        cur.execute(sql_insert_query4, insert_tuple_5)
                        mydb.commit()
                        cur1.count=cur1.count+1
                        cur1=cur1.next  

                        sql_insert_query4 = """ INSERT INTO mysamp(Name,Department,room,date,session,status) VALUES (%s, %s, %s, %s, %s,%s)"""
                        a=cur2.data
                        b=cur2.department
                        c=room[i]
                        d=days
                        f="T"
                        insert_tuple_5 = (a,b,c,d,e,f)
                        cur.execute(sql_insert_query4, insert_tuple_5)
                        mydb.commit()
                        cur2.count=cur2.count+1
                        cur2=cur2.next
                    if x[i]==4:

                        sql_insert_query4 = """ INSERT INTO mysamp(Name,Department,room,date,session,status) VALUES (%s, %s, %s,%s, %s, %s)"""
                        a=cur1.data
                        b=cur1.department
                        c=room[i]
                        d=days
                        f="P"
                        insert_tuple_5 = (a,b,c,d,e,f)
                        cur.execute(sql_insert_query4, insert_tuple_5)
                        mydb.commit()
                        cur1.count=cur1.count+1
                        cur1=cur1.next

                        sql_insert_query4 = """ INSERT INTO mysamp(Name,Department,room,date,session,status) VALUES (%s, %s, %s, %s,%s,%s)"""
                        a=cur1.data
                        b=cur1.department
                        c=room[i]
                        d=days
                        f="P"
                        insert_tuple_5 = (a,b,c,d,e,f)
                        cur.execute(sql_insert_query4, insert_tuple_5)
                        mydb.commit()
                        cur1.count=cur1.count+1
                        cur1=cur1.next

                        sql_insert_query4 = """ INSERT INTO mysamp(Name,Department,room,date,session,status) VALUES (%s, %s, %s,%s, %s, %s)"""
                        a=cur2.data
                        b=cur2.department
                        c=room[i]
                        d=days
                        f="T"
                        insert_tuple_5 = (a,b,c,d,e,f)
                        cur.execute(sql_insert_query4, insert_tuple_5)
                        mydb.commit()
                        cur2.count=cur2.count+1
                        cur2=cur2.next

                        sql_insert_query4 = """ INSERT INTO mysamp(Name,Department,room,date,session,status) VALUES (%s, %s, %s,%s, %s, %s)"""
                        a=cur2.data
                        b=cur2.department
                        c=room[i]
                        d=days
                        f="T"
                        insert_tuple_5 = (a,b,c,d,e,f)
                        cur.execute(sql_insert_query4, insert_tuple_5)
                        mydb.commit()
                        cur2.count=cur2.count+1
                        cur2=cur2.next
    #********SWAPPING DUTIES FOR PERMANENT WITH TEMPORARY TEACHERS********    
            db3=mydb.cursor()
            n1="2019-05-25"
            shift_name=[]
            date_total=[]
            shift_depart=[]
            shift_duty=[]
            shift_date=[]
            shift_session=[]
            shift_status=[]
            #*************** DETAILS OF PERMANENT TEACHERS***********
            db3.execute("SELECT * FROM mysamp WHERE date>%s AND status=%s" , (n1,"P"))
            records3=db3.fetchall()
            for row in records3:
                shift_name.append(row[0])
                shift_depart.append(row[1])
                shift_duty.append(row[2])
                shift_date.append(row[3])
                shift_session.append(row[4])
                shift_status.append(row[5])
            #**********NO OF DATES***********
            db3.execute("SELECT distinct(date) FROM mysamp WHERE date>%s",(n1,))
            records4=db3.fetchall()
            for row in records4:
                date_total.append(row[0])
            #*********** REAL DEAL***********
            for jj in range(0,len(date_total)):
                db3.execute("SELECT Name from mysamp where date=%s and status=%s",(date_total[jj],"T"))
                read3=db3.fetchall()
                for kk in range(0,len(shift_name)):
                    flag=0
                    if shift_date[kk]==date_total[jj]:
                        while(1):
                            for row in read3:
                                if cur2.data==row:
                                    flag=1
                            if flag==0:
                                sql_insert_query4 = """ INSERT INTO mysamp(Name,Department,room,date,session,status) VALUES (%s, %s, %s, %s, %s,%s)"""
                                a=cur2.data
                                b=cur2.department
                                c=shift_duty[kk]
                                d=shift_date[kk]
                                e=shift_session[kk]
                                f="replace"
                                insert_tuple_5 = (a,b,c,d,e,f)
                                cur.execute(sql_insert_query4, insert_tuple_5)
                                mydb.commit()
                                cur2.count=cur2.count+1
                                cur2=cur2.next
                                #print("DONE")
                                break;
                            else:
                                cur2=cur2.next

            db3.execute("DELETE FROM mysamp WHERE date>%s AND status=%s",(n1,"P")) 
    #********SWAPPING DUTIES FOR PERMANENT WITH TEMPORARY TEACHERS********    
            db3=mydb.cursor()
            n1="2019-05-25"
            shift_name=[]
            date_total=[]
            shift_depart=[]
            shift_duty=[]
            shift_date=[]
            shift_session=[]
            shift_status=[]
            #*************** DETAILS OF PERMANENT TEACHERS***********
            db3.execute("SELECT * FROM mysamp WHERE date>%s AND status=%s" , (n1,"P"))
            records3=db3.fetchall()
            for row in records3:
                shift_name.append(row[0])
                shift_depart.append(row[1])
                shift_duty.append(row[2])
                shift_date.append(row[3])
                shift_session.append(row[4])
                shift_status.append(row[5])
            #**********NO OF DATES***********
            db3.execute("SELECT distinct(date) FROM mysamp WHERE date>%s",(n1,))
            records4=db3.fetchall()
            for row in records4:
                date_total.append(row[0])
            #*********** REAL DEAL***********
            for jj in range(0,len(date_total)):
                db3.execute("SELECT Name from mysamp where date=%s and status=%s",(date_total[jj],"T"))
                read3=db3.fetchall()
                for kk in range(0,len(shift_name)):
                    flag=0
                    if shift_date[kk]==date_total[jj]:
                        while(1):
                            for row in read3:
                                if cur2.data==row:
                                    flag=1
                            if flag==0:
                                sql_insert_query4 = """ INSERT INTO mysamp(Name,Department,room,date,session,status) VALUES (%s, %s, %s, %s, %s,%s)"""
                                a=cur2.data
                                b=cur2.department
                                c=shift_duty[kk]
                                d=shift_date[kk]
                                e=shift_session[kk]
                                f="replace"
                                insert_tuple_5 = (a,b,c,d,e,f)
                                cur.execute(sql_insert_query4, insert_tuple_5)
                                mydb.commit()
                                cur2.count=cur2.count+1
                                cur2=cur2.next
                                #print("DONE")
                                break;
                            else:
                                cur2=cur2.next

            db3.execute("DELETE FROM mysamp WHERE date>%s AND status=%s",(n1,"P")) 





    #***********MAIN FUNCTION**************            
    def harsh():
        list1 = CircularLinkedList()
        list2=CircularLinkedList()
        list3=CircularLinkedList()
        for i in range(0,len(name_p)):
                list1.append(name_p[i],department_p[i],0)
        for i in range(0,len(name_t)):
                list2.append(name_t[i],department_t[i],0)
        for i in range(0,len(name_s)):
                list3.append(name_s[i],"Dept. Supt.",0)


        list1.newlist(list1.head,list2.head)
        list3.newlist1(list3.head)
    
    #print("finish")
    #****************** function to give teachers chance****************#
    #*****************Code creating the excel file*****************
    harsh()
    course_dict= { 582: "PS",583 : "LS", 554 :"BMS", 556 :"BOTANY",557 : "CHEM", 570: "CS", 558: "ELECT",
                               563 : "MATHS", 567 : "PHY", 569 : "ZOOLGY", 504 : "BCOM"}
     

    #print(path)   
    for i in my_objects:
        ##print(i.date)
        ##print(i.session)
        #print(i.date,i.session)
        filename = str(path)+"/"+str(i.date)+str(i.session[0])+".xlsx"
        filename_attendance = str(path)+"/"+str(i.date)+str(i.session[0])+"ATND."+".xlsx"

        ##print(filename)
        workbook = xlsxwriter.Workbook(filename) 
        attendance=xlsxwriter.Workbook(filename_attendance) 

        helpsheet = workbook.add_worksheet("Cheat sheet") 
        helpsheet.write(0,0,"Date-" + str(i.date))  
        helpsheet.write(0,6,"Session-" + str(i.session))
        helpsheet_index=1
        columns=0
        capacity=0
        rows=0
        attrow=0
        a=0
        b=0
        a_arr= i.a_arr
        b_arr = i.b_arr
        a_course= i.a_course
        b_course = i.b_course
        a_year= i.a_year
        b_year= i.b_year
        papercode_count=0;
        rollno_a = [];
        rollno_b=[];
        current_a=0
        current_b=0
        check_a=''
        check_b=''
        for j in i.room_used:
            roomno = j
            #print("Room",j)
            student_course_l=[];
            student_course_r=[];
            year_l=[]
            year_r=[]
            change_l=[]
            change_r=[]
            flag_l=0;
            flag_r=0;
            temp_l=0
            temp_r=0
            stopval_l=0 # too stop writting same course two times
            stop_arr_l=[];
            stopval_r=0 # too stop writting same course two times
            stop_arr_r=[];

            for k in my_room_objects:
                if(k.no == roomno):
                    columns= k.columns
                    capacity= k.capacity
                    rows = k.total_rows
                else:pass;       
            if(a < len(a_arr)):
                if len(rollno_a)>=rows:
                    student_course_l.append(current_a)
                    year_l.append(check_a)
                    change_l.append(rows)
                elif len(rollno_a)< rows and len(rollno_a)>0:
                    student_course_l.append(current_a)
                    year_l.append(check_a)
                    flag_l=1
                    change_l.append(len(rollno_a))
                    # #print(current_a,j)
                    while(len(rollno_a)<rows):
                        if(a < len(a_arr)):
                            query="SELECT University_rollno from  student_details where Paper_code = "+str(a_arr[a])+" and Course_Code ="+str(a_course[a])+" and Paper_year = '"+ a_year[a]+"'"        
                            ##print(query)
                            students= pd.read_sql_query(query,mydb);
                            student= pd.DataFrame(students)
                            values = student.to_numpy(dtype = 'int')
                            for n in values:
                                rollno_a.append(int(n));

                            temp_l=len(rollno_a)
                            if len(rollno_a)>=rows:
                                change_l.append(rows)
                            else:
                                change_l.append(temp_l)

                            student_course_l.append(a_course[a])
                            year_l.append(a_year[a])
                            #             #print(a_course[a],j)
                            current_a= a_course[a]
                            check_a=a_year[a]
                            a=a+1
                        else:
                            break;
                elif len(rollno_a)==0:
                    while(len(rollno_a)<rows):
                        if(a < len(a_arr)):
                            flag=1
                            query="SELECT University_rollno from  student_details where Paper_code = "+str(a_arr[a])+" and Course_Code ="+str(a_course[a])+" and Paper_year = '"+ a_year[a]+"'"        
                            ##print(query)
                            students= pd.read_sql_query(query,mydb);
                            student= pd.DataFrame(students)
                            values = student.to_numpy(dtype = 'int')
                            for n in values:
                                rollno_a.append(int(n));
                            temp_l=len(rollno_a)
                            if len(rollno_a)>=rows:
                                change_l.append(rows)
                            else:
                                change_l.append(temp_l)    
                            student_course_l.append(a_course[a])
                            year_l.append(a_year[a])
                            #             #print(a_course[a],j)
                            current_a= a_course[a]
                            check_a=a_year[a]
                            a=a+1
                        else:
                            break;
                else:pass
            else:
                if(len(rollno_a)!=0):
                    flag_l=2
                    student_course_l.append(current_a)
                    year_l.append(check_a)
                    temp_l=len(rollno_a)
                    if len(rollno_a)>=rows:
                        change_l.append(rows)
                    else:
                        change_l.append(temp_l)  

                else: pass


            if(b < len(b_arr)):
                if len(rollno_b)>=rows:
                    student_course_r.append(current_b)
                    year_r.append(check_b)
                    change_r.append(rows)
                elif len(rollno_b)< rows and len(rollno_b)>0:
                    student_course_r.append(current_b)
                    year_r.append(check_b)
                    flag_r=1
                    change_r.append(len(rollno_b))
                    # #print(current_a,j)
                    while(len(rollno_b)<rows):
                        if(b < len(b_arr)):
                            query="SELECT University_rollno from  student_details where Paper_code = "+str(b_arr[b])+" and Course_Code ="+str(b_course[b])+" and Paper_year = '"+ b_year[b]+"'"        
                            ##print(query)
                            students= pd.read_sql_query(query,mydb);
                            student= pd.DataFrame(students)
                            values = student.to_numpy(dtype = 'int')
                            for n in values:
                                rollno_b.append(int(n));
                            temp_r=len(rollno_b)
                            if len(rollno_b)>=rows:
                                change_r.append(rows)
                            else:
                                change_r.append(temp_r)    
                            student_course_r.append(b_course[b])
                            year_r.append(b_year[b])
                   #        #print(a_course[a],j)
                            current_b= b_course[b]
                            check_b=b_year[b]
                            b=b+1
                        else:
                            break;
                elif len(rollno_b)==0:
                    while(len(rollno_b)<rows):
                        if(b < len(b_arr)):
                            flag_r=1
                            query="SELECT University_rollno from  student_details where Paper_code = "+str(b_arr[b])+" and Course_Code ="+str(b_course[b])+" and Paper_year = '"+ b_year[b]+"'"        
                            ##print(query)
                            students= pd.read_sql_query(query,mydb);
                            student= pd.DataFrame(students)
                            values = student.to_numpy(dtype = 'int')
                            for n in values:
                                rollno_b.append(int(n));
                            temp_r=len(rollno_b)
                            if len(rollno_b)>=rows:
                                change_r.append(rows)
                            else:
                                change_r.append(temp_r)        
                            student_course_r.append(b_course[b])
                            year_r.append(b_year[b])
                   #        #print(a_course[a],j)
                            current_b= b_course[b]
                            check_b=b_year[b]
                            b=b+1
                        else:
                            break;
                else:pass
            else:
                if(len(rollno_b)!=0):
                    flag_r=2
                    student_course_r.append(current_b)
                    year_r.append(check_b)
                    temp_r=len(rollno_b)
                    if len(rollno_b)>=rows:
                        change_r.append(rows)
                    else:
                        change_r.append(temp_r)  
                else: pass;



            bold = workbook.add_format({'bold': True})   
            boldatt = attendance.add_format({'bold': True})   
            font = workbook.add_format()
            fontatt= attendance.add_format()
            border = attendance.add_format({'border': 1})
            font.set_font_size(9)
            worksheet = workbook.add_worksheet("Room No-"+ str(roomno)) 


            worksheet.set_landscape()
            worksheet.write(0,0,"Date-" + str(i.date))  
            worksheet.write(0,7,"Session-" + str(i.session))  
            worksheet.write(1,4,"Room no-" + str(roomno), bold)
            l_arr=""
            r_arr=""
            for x in range(0,len(student_course_l)):
                if(x!=0):
                    l_arr+= ","+str(course_dict[student_course_l[x]])+"-"+year_l[x]
                else:
                    l_arr+=str(course_dict[student_course_l[x]])+"-"+year_l[x]
                    ##print(l_arr)

            for x in range(0,len(student_course_r)):
                if(x!=0):
                    r_arr+= ","+str(course_dict[student_course_r[x]])+"-"+year_r[x]
                else:
                    r_arr+= str(course_dict[student_course_r[x]])+"-"+year_r[x]
                    ##print(r_arr)
            row = 2
            col = 1

            # Iterate over the data and write it out row by row. 
            for k in range(columns):
                worksheet.write(row, col, "   Row "+str(k+1)) 
                worksheet.write(row, col + 1, "   Row "+str(k+1)) 
                col+=2
            row = 3
            col = 1

            # Iterate over the data and write it out row by row. 
            for k in range(columns):
                if(flag_l==0):
                    if(len(rollno_a)>0):
                        worksheet.write(row, col, str(course_dict[student_course_l[0]])+" - "+str(year_l[0]))
                elif(flag_l==1):
                    for val in range(0 , len(change_l)):
                        t=change_l[val]/(rows/columns)
                        t1= math.floor(t)
                        if(t>t1):
                            if(t>=k):
                                worksheet.write(row, col, str(course_dict[student_course_l[val]])+" - "+str(year_l[val]))
                                break;
                        else:
                            stopval_l=1
                            stop_arr_l.append(val)
                            if(t>k):
                                worksheet.write(row, col, str(course_dict[student_course_l[val]])+" - "+str(year_l[val]))

                                break;

                    ##print(test)
                else:
                    t=change_l[0]/(rows/columns)
                    t1= math.floor(t)
                    if(t>t1):
                        if(t1>=k):
                            worksheet.write(row, col, str(course_dict[student_course_l[0]])+" - "+str(year_l[0]))
                    else:
                        if(t1>k):
                            worksheet.write(row, col, str(course_dict[student_course_l[0]])+" - "+str(year_l[0]))



                if(flag_r==0):
                    if(len(rollno_b)>0):
                        worksheet.write(row, col+1, str(course_dict[student_course_r[0]])+" - "+str(year_r[0]))
                elif(flag_r==1):
                    for val in range(0 , len(change_r)):
                        t=change_r[val]/(rows/columns)
                        t1= math.floor(t)
                        if(t>t1):
                            if(t>=k):
                                worksheet.write(row, col+1, str(course_dict[student_course_r[val]])+" - "+str(year_r[val]))
                                break;
                        else:
                            stopval_r=1
                            stop_arr_r.append(val)
                            if(t>k):
                                worksheet.write(row, col+1, str(course_dict[student_course_r[val]])+" - "+str(year_r[val]))
                                break;

                    ##print(test)
                else:
                    t=change_r[0]/(rows/columns)
                    t1= math.floor(t)
                    if(t>t1):
                        if(t1>=k):
                            worksheet.write(row, col+1, str(course_dict[student_course_r[0]])+" - "+str(year_r[0]))
                    else:
                        if(t1>k):
                            worksheet.write(row, col+1, str(course_dict[student_course_r[0]])+" - "+str(year_r[0]))


                col+=2



            extra_detail_index=  int(rows/columns)+3
            index=0
            col=1
            actual_l=0
            doub_l=0
            if(len(rollno_a)!=0):
                chng_tmp_l=change_l[0]
            for l in range(columns):

                index=l*int(rows/columns)
                row=4

                for m in range(int(rows/columns)):
                    if flag_l!=1:
                        if(row> extra_detail_index):
                            extra_detail_index= row
                            #print(extra_detail_index)
                        if(len(rollno_a) > index):
                            worksheet.write(row, col, str(rollno_a[index]),font)
                            worksheet.set_column(row, col,10 )
                        if(len(rollno_a) <= index):
                            worksheet.write(row, col, None)
                            worksheet.set_column(row, col, 10)
                    else:
                        if index == chng_tmp_l and actual_l< len(change_l)-1:
                            if(stopval_l == 1 and (actual_l) == stop_arr_l[doub_l]):
                                actual_l+=1
                                if(doub_l<len(stop_arr_l)-1):
                                    doub_l+=1
                            else:
                                worksheet.write(row, col, str(course_dict[student_course_l[actual_l+1]])+"-"+str(year_l[actual_l+1]))
                                worksheet.set_column(row, col,10 )
                                actual_l+=1
                                row+=1
                               # #print(actual_l,"actual")
                                chng_tmp_l=change_l[actual_l]
                                ##print(chng_tmp_l,"new val")
                        if(len(rollno_a) > index):
                            worksheet.write(row, col, str(rollno_a[index]),font)
                            worksheet.set_column(row, col,10 )
                        if(len(rollno_a) <= index):
                            worksheet.write(row, col, None)
                            worksheet.set_column(row, col, 10)
                        if(row> extra_detail_index):
                            extra_detail_index= row
                            #print(extra_detail_index)


                    row+=1      
                    index= index+1

                worksheet.set_column(row, 8,10 )  
                col+=2 


            index=0
            col=2
            actual_r=0
            doub_r=0
            if(len(rollno_b)!=0):
                chng_tmp_r=change_r[0]
            for l in range(columns):

                index=l*int(rows/columns)
                row=4

                for m in range(int(rows/columns)): 
                    if flag_r!=1:
                        if(row> extra_detail_index):
                            extra_detail_index= row
                            #print(extra_detail_index)
                        if(len(rollno_b) > index):
                            worksheet.write(row, col, str(rollno_b[index]),font)
                            worksheet.set_column(row, col,10 )
                        if(len(rollno_b) <= index):
                            worksheet.set_column(row, col,10 )
                            worksheet.write(row, col, None)
                    else:
                        if index == chng_tmp_r and actual_r< len(change_r)-1:
                            if(stopval_r == 1 and (actual_r) == stop_arr_r[doub_r]):
                                actual_r+=1
                                if(doub_r<len(stop_arr_r)-1):
                                    doub_r+=1
                            else:
                                worksheet.write(row, col, str(course_dict[student_course_r[actual_r+1]])+"-"+str(year_r[actual_r+1]))
                                worksheet.set_column(row, col,10 )
                                actual_r+=1
                                row+=1
                                ##print(actual_l,"actual")
                                chng_tmp_r=change_r[actual_r]
                               # #print(chng_tmp_l,"new val")
                        if(len(rollno_b) > index):
                            worksheet.write(row, col, str(rollno_b[index]),font)
                            worksheet.set_column(row, col,10 )
                        if(len(rollno_b) <= index):
                            worksheet.set_column(row, col,10 )
                            worksheet.write(row, col, None)
                        if(row> extra_detail_index):
                            extra_detail_index= row
                            #print(extra_detail_index)


                    row+=1      
                    index= index+1

                worksheet.set_column(row, 8,10 )  
                col+=2 

            query="SELECT Name from  mysamp where room = "+str(roomno)+" and date = '"+str(i.date)+"' and session = '"+ str(i.session)+"'"        
            ##print(query)
            teach= pd.read_sql_query(query,mydb);
            teacher=pd.DataFrame(teach["Name"])
            data_arr= teacher.to_numpy(dtype = 'str')
            staff = [];
            check=" this is for help"
            teachers=""
            for teaching in data_arr:
                staff.append(teaching)
            ##print(teach)
            for x in range(len(staff)):
                actual=check.join(staff[x])
                if(x<len(staff)-1):
                    teachers += actual+" ,"
                else:
                    teachers += actual

            ##print(teachers)
            row=extra_detail_index+2
            font.set_font_size(11)
            worksheet.write(row+1,1,"Left Side - ",font)
            worksheet.write(row+2,1,"Right Side -",font)
            font.set_font_size(9)
            worksheet.write(row+1,2,l_arr,font)
            worksheet.write(row+2,2,r_arr,font)
            font.set_font_size(11)
            worksheet.write(row+3,1,"On duty -",font)
            font.set_font_size(9)
            worksheet.write(row+3,2,teachers,font)

            font.set_font_size(9)
            worksheet.write(row+5,1,"Course",bold)
            worksheet.write(row+5,2,"Total",bold)
            row= extra_detail_index+8

            for indexes in range(len(student_course_l)):

                if(indexes==0):
                    font.set_font_size(11)
                    worksheet.write(row+indexes,1,str(course_dict[student_course_l[indexes]])+"-"+str(year_l[indexes]),font)
                    font.set_font_size(9)
                    worksheet.write(row+indexes,2,change_l[indexes],font)
                else:
                    temp= change_l[indexes]- change_l[indexes-1]
                    font.set_font_size(11)
                    worksheet.write(row+indexes,1,str(course_dict[student_course_l[indexes]])+"-"+str(year_l[indexes]),font)
                    font.set_font_size(9)
                    worksheet.write(row+indexes,2,temp,font)

            row= row+ len(student_course_l)
            for indexes in range(len(student_course_r)):

                if(indexes==0):
                    font.set_font_size(11)
                    worksheet.write(row+indexes,1,str(course_dict[student_course_r[indexes]])+"-"+str(year_r[indexes]),font)
                    font.set_font_size(9)
                    worksheet.write(row+indexes,2,change_r[indexes],font)
                else:
                    temp= change_r[indexes]- change_r[indexes-1]
                    font.set_font_size(11)
                    worksheet.write(row+indexes,1,str(course_dict[student_course_r[indexes]])+"-"+str(year_r[indexes]),font)
                    font.set_font_size(9)
                    worksheet.write(row+indexes,2,temp,font)

            #making CHEAT SHEET******************************************     
            helpsheet.write(helpsheet_index,1,"Room no-" + str(roomno), bold)          
            helpsheet_index= helpsheet_index+1    
            for indexes in range(len(student_course_l)):

                if(indexes==0):
                    font.set_font_size(11)
                    helpsheet.write(helpsheet_index+indexes,1,str(course_dict[student_course_l[indexes]])+"-"+str(year_l[indexes]),font)
                    font.set_font_size(9)
                    helpsheet.write(helpsheet_index+indexes,2,change_l[indexes],font)
                else:
                    temp= change_l[indexes]- change_l[indexes-1]
                    font.set_font_size(11)
                    helpsheet.write(helpsheet_index+indexes,1,str(course_dict[student_course_l[indexes]])+"-"+str(year_l[indexes]),font)
                    font.set_font_size(9)
                    helpsheet.write(helpsheet_index+indexes,2,temp,font)

            helpsheet_index= helpsheet_index+ len(student_course_l)


            for indexes in range(len(student_course_r)):

                if(indexes==0):
                    font.set_font_size(11)
                    helpsheet.write(helpsheet_index+indexes,1,str(course_dict[student_course_r[indexes]])+"-"+str(year_r[indexes]),font)
                    font.set_font_size(9)
                    helpsheet.write(helpsheet_index+indexes,2,change_r[indexes],font)
                else:
                    temp= change_r[indexes]- change_r[indexes-1]
                    font.set_font_size(11)
                    helpsheet.write(helpsheet_index+indexes,1,str(course_dict[student_course_r[indexes]])+"-"+str(year_r[indexes]),font)
                    font.set_font_size(9)
                    helpsheet.write(helpsheet_index+indexes,2,temp,font)
            helpsheet_index= helpsheet_index+ len(student_course_r)+2


            #making ATTENDANCE SHEET********************************
            attrow=5
            for indexes in range(len(student_course_l)):

                attsheet = attendance.add_worksheet("Room No-"+ str(roomno)+" ("+str(indexes+1)+")")
                attsheet.set_column(1, 1,22)
                attsheet.set_column(1, 2,22)
                attsheet.write(0,1,"AND College" ,boldatt)
                attsheet.write(1,0,"Date-" + str(i.date))
                attsheet.write(1,1,"Room no-" + str(roomno))
                attsheet.write(1,2,"Session-" + str(i.session))
                attsheet.write(2,0,"Course-" + str(course_dict[student_course_l[indexes]])+"-"+year_l[indexes])  
                attsheet.write(4,0,"Roll No",border)
                attsheet.write(4,1,"Answer Sheet No", border)
                attsheet.write(4,2,"Signature",border)

                if(indexes==0):

                    temp=change_l[indexes]
                    for t in range (temp):
                        attsheet.set_column(attrow+t, 0,22 )
                      #  attsheet.write(attrow+t, 0, "",border)
                        attsheet.write(attrow+t, 1, "",border)
                        attsheet.write(attrow+t, 2, "",border)
                        attsheet.write(attrow+t, 0, str(rollno_a[t]),border)

                else:
                    temp= change_l[indexes]- change_l[indexes-1]
                    start= change_l[indexes-1]
                    for t in range (temp):
                        attsheet.set_column(attrow+t, 0,22)
                        attsheet.write(attrow+t, 1, "",border)
                        attsheet.write(attrow+t, 2, "",border)
                        attsheet.write(attrow+t, 0, str(rollno_a[t+start]),border)

                attsheet.write(40,0,"Invigilator's Name")
                attsheet.write(40,1,"Invigilator's Sign")
                for val in range(len(staff)):
                    actual=check.join(staff[val])
                    attsheet.write(val+41, 0, actual)

            for indexes in range(len(student_course_r)):
                attsheet = attendance.add_worksheet("Room No-"+ str(roomno)+" ("+str(len(student_course_l)+indexes+1)+")")
                attsheet.set_column(1, 1,22)
                attsheet.set_column(1, 2,22)
                attsheet.write(0,1,"AND College" ,boldatt)
                attsheet.write(1,0,"Date-" + str(i.date))
                attsheet.write(1,1,"Room no-" + str(roomno))
                attsheet.write(1,2,"Session-" + str(i.session))
                attsheet.write(2,0,"Course-" + str(course_dict[student_course_r[indexes]])+"-"+year_r[indexes])  
                attsheet.write(4,0,"Roll No",border)
                attsheet.write(4,1,"Answer Sheet No", border)
                attsheet.write(4,2,"Signature",border)

                if(indexes==0):

                    temp=change_r[indexes]
                    for t in range (temp):
                        attsheet.set_column(attrow+t, 0,22 )
                      #  attsheet.write(attrow+t, 0, "",border)
                        attsheet.write(attrow+t, 1, "",border)
                        attsheet.write(attrow+t, 2, "",border)
                        attsheet.write(attrow+t, 0, str(rollno_b[t]),border)

                else:
                    temp= change_r[indexes]- change_r[indexes-1]
                    start= change_r[indexes-1]
                    for t in range (temp):
                        attsheet.set_column(attrow+t, 0,22)
                        attsheet.write(attrow+t, 1, "",border)
                        attsheet.write(attrow+t, 2, "",border)
                        attsheet.write(attrow+t, 0, str(rollno_b[t+start]),border)

                attsheet.write(40,0,"Invigilator's Name")
                attsheet.write(40,1,"Invigilator's Sign")
                for val in range(len(staff)):
                    actual=check.join(staff[val])
                    attsheet.write(val+41, 0, actual)



            rollno_a= rollno_a[rows::]
            rollno_b= rollno_b[rows::] 

        if(len(i.room_used)!=0):
            workbook.close() 
            attendance.close()
        else:pass;
                ##print(student_course)
    filename_teacher = str(path)+"/"+"Teacher_duties."+".xlsx"
    teacher_duty_file= xlsxwriter.Workbook(filename_teacher)    
    b = teacher_duty_file.add_format({'bold': True}) 
    query="SELECT distinct(Name) from  mysamp "        
            ##print(query)
    teach= pd.read_sql_query(query,mydb);
    teacher=pd.DataFrame(teach["Name"])
    data_arr= teacher.to_numpy(dtype = 'str')
    staff = [];
    check=" this is for help"
    teachers=[];
    for teaching in data_arr:
        staff.append(teaching)
    for x in range(len(staff)):
        teachers.append(check.join(staff[x]) )     
    teacher_duty =  teacher_duty_file.add_worksheet("Duty dates")
    teacher_duty.write(0,1,"AND College" ,b)

    teacher_duty.set_column(0,0,7)
    teacher_duty.set_column('B:B',22)
    teacher_duty.set_column('C:C',12)
    teacher_duty.set_column('D:D',12)
    teacher_duty.set_column('E:E',12)
    teacher_duty.set_column('F:F',12)
    teacher_duty.set_column('G:G',12)
    teacher_duty.set_column('H:H',12)
    teacher_duty.set_column('I:I',12)
    teacher_duty.write(1,0,"S.No.",b )
    teacher_duty.write(1,1,"Teacher Name",b )
    teacher_duty.write(1,2,"Date / Room alloted",b)
    dutrow=2

    for v in range(len(teachers)):
        dutcol=0
        teacher_duty.write(dutrow+v,dutcol,str(v+1)+".")
        teacher_duty.write(dutrow+v,dutcol+1,teachers[v])
        query_n="SELECT date,session,room from  mysamp where Name = '" + teachers[v]+"';"        
        #print(query_n)
        duty_dat= pd.read_sql_query(query_n,mydb);
        duty_d=pd.DataFrame(duty_dat["date"])
        duty_s=pd.DataFrame(duty_dat["session"])
        duty_r=pd.DataFrame(duty_dat["room"])
        duty_date= duty_d.to_numpy(dtype = 'str')
        duty_session= duty_s.to_numpy(dtype = 'str')
        duty_room= duty_r.to_numpy(dtype = 'str')
        d_date = []
        d_session=[]
        d_room=[]
        check=" this is for help"
        for val in range(len(duty_date)):
            d_date.append(duty_date[val])
            d_session.append(duty_session[val])
            d_room.append(duty_room[val])
        dutcol=2    
        for x in range(len(d_date)):
            if(check.join(d_session[x])=='EVENING'):
                teacher_duty.write(dutrow+v,dutcol+x,check.join(d_date[x])[5:]+"E /"+ str(check.join(d_room[x])))
            else:
                teacher_duty.write(dutrow+v,dutcol+x,check.join(d_date[x])[5:]+" / "+ str(check.join(d_room[x])))
          #  duty_d.append(check.join(d_date[x]) )     
           # duty_s.append( )    



    teacher_duty_file.close()
    #print("Directory '% s' created" % directory) 
    return 0;
#/home/chirag/Desktop
                    
                    

    
 







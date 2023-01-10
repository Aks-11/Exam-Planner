#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re

import xlrd
import mysql.connector
import parse
import pandas as pd
import datetime
import time
from collections import namedtuple
from mysql.connector import Error


# In[2]:


try:
    mydb = mysql.connector.connect( host="localhost",  user="root", passwd="root",database="exam1")
    if mydb.is_connected():
        cur = mydb.cursor(prepared=True)
        print("db displayed sucessfully")
    else:
        print("error while connecting to database")
    cur=mydb.cursor()
    cur.execute("DROP TABLE IF EXISTS main;")
    cur.execute("DROP TABLE IF EXISTS teachers;")
    cur.execute("DROP TABLE IF EXISTS course;")
    cur.execute("DROP TABLE IF EXISTS student_details;")
    #*****************************creating tables**************************************
    cur.execute("CREATE TABLE main (date varchar(10),papercode int(8),PRIMARY KEY(date,papercode))") 
    cur.execute("CREATE TABLE teachers(Sno int(3),Name varchar(50),Mobile_no bigint(10),Email varchar(30),Department varchar(20),Status varchar(15))")
    cur.execute("CREATE TABLE course (Course_Code int(20),Year char(6),Semester char(6),Paper_Code int(9),Paper_Name varchar(150),Sum int(6),Date date,Session varchar(50))")
    cur.execute("CREATE TABLE student_details(Paper_Code int(20),Paper_year char(6),Course_code int(30),Year char(6),Semester char(6),Paper_name varchar(150),College_rollno varchar(60),University_rollno bigint(150),Name varchar(70))")
    
    #OPENING THE PDF FILE 
    file = 'datesheet.pdf'
    #working module*****************DATE FINDER************************//\\*******************
    date_finder=re.compile(r'(\d{1,2}(st)?(nd)?(rd)?(th)?\s+(April|May|June))')
    #********************PAPER CODE FINDER*************
    code_finder= re.compile(r'(\d{8})')
#************************TRAVERSING WITH PDFPLUMBER PAGE WISE THEN LINE WISE ****************
#vibhu course list into db
    excel2="course12 (1).xlsx"
    book2=xlrd.open_workbook(excel2)
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
           



    with pdfplumber.open(file) as pdf:
        pages = pdf.pages
        for page in pdf.pages:
            text = page.extract_text()
            for line in text.split('\n'):
        
                if date_finder.search(line):
                    x=date_finder.search(line).group(1)
                if code_finder.search(line):
                    y=code_finder.search(line).group(1)
                    sql_insert_query = """ INSERT INTO main(date, papercode) VALUES (%s,%s)"""

                    insert_tuple_1 = (x,y)
                

                    cur.execute(sql_insert_query, insert_tuple_1)
                    mydb.commit()
                    print("Data inserted successfully into main table using the prepared statement")
      # MAIN CODE
      #TEACHERS EXCEL SHEET INTO DB              
    excel1="teacher_list.xlsx"
    
    book1=xlrd.open_workbook(excel1)
    
    sheet=book1.sheet_by_index(0)
    
    for r in range(1,sheet.nrows):
        
        sql_insert_query1 = """ INSERT INTO teachers(Sno, Name, Mobile_no, Email,Department,Status) VALUES (%s, %s, %s, %s, %s, %s)"""
        
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
        
   
# STUDENTS DATA INTO DB 
    excel3="students12 (2).xlsx"        
    book3=xlrd.open_workbook(excel3)
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



# COURSE LIST INTO DB not needed
excel2="course.xlsx"
 
name=["PS","LS","bms","CS","Botany","Chemistry","Electronics","Mathematics","Physics","Zoology","B.Com (H)"]
 
for i in range(0,len(name)):
     
     book2=xlrd.open_workbook(excel2)
     
     sheet=book2.sheet_by_name(name[i])

     for r in range(1,sheet.nrows):
         x=0
 
         a=sheet.cell(r,1).value
 
         b=sheet.cell(r,2).value
 
         c=sheet.cell(r,3).value
 
         d=sheet.cell(r,4).value 
 
         e=sheet.cell(r,5).value
         while r<sheet.nrows-1:
             if sheet.cell(r+1,8).value=="TOTAL" :
                 break
        
             else:
                 x=x+sheet.cell(r+1,8).value
                 r=r+1

     
         if(a):
             sql_insert_query2 = """ INSERT INTO course(Course_Code,Year,Semester,Paper_Code,Paper_Name,Sum) VALUES (%s, %s, %s,%s, %s, %s)"""
 
             insert_tuple_3 = (a,b,c,d,e,x)
     
             cur.execute(sql_insert_query2, insert_tuple_3)
     
             mydb.commit()
     
             print("Data inserted successfully into course table using the prepared statement")
         







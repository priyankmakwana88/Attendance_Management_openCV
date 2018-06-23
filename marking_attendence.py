#!/usr/bin/env python3

#IMPORTING LIBRARIES
import cv2
from xlrd import open_workbook
from xlutils.copy import copy
import face_recognition
import os
import datetime

#IMPORTING SELF-MADE FUNCTIONS
from face_in_class_live import face_in_class_live

#GENERATING TODAY'S DATE
date_format=datetime.date.today()
day=date_format.day
month=date_format.month
year=date_format.year

current_date=str(day)+'/'+str(month)+'/'+str(year)
#print(current_date)


#ACCESSING DATABASE
workbook = open_workbook("attendence_database.xls")
edit_sheet = copy(workbook)
s=workbook.sheets()[0]
excel = edit_sheet.get_sheet(0)


#READING XLS DATA
values = []
for row in range(s.nrows):
	col_value = []
	for col in range(s.ncols):
		value  = (s.cell(row,col).value)
		try : value = str(int(value))
		except : pass
		col_value.append(value)
	values.append(col_value)
#print (values)


#ASSIGNING AND CHECKING THE PRESENCE OF TODAY"S DATE IN DATABASE
status='not_marked'
if current_date not in values[0][-1]:
	total_col=s.ncols
	excel.write(0,total_col,current_date)
else:
	#print("ATTENDANCE ALREADY MARKED")
	status='marked'


#MARKING ATTENDANCE FOR TODAY
if status=='not_marked':
	#LOADING ENCODINGS OF THE STUDENT CURRENTLY IN CLASS
	count=face_in_class_live()
	current_class_encoding=[]
	for i in range(1,count+1):
		student = face_recognition.load_image_file("current_class/student"+i+".jpeg")
		student_encoding = face_recognition.face_encodings(student)[0]	
		current_class_encoding.append(student_encoding)

	'''#markdown#'''
	
	
	#excel.write(count+1,0,count+1)
	#excel.write(count+1,1,s_roll_number)
	#excel.write(count+1,2,s_fname)
	#excel.write(count+1,3,s_lname)
	edit_sheet.save('attendence_database.xls')

else:
	print("Attendence marked for today!!")



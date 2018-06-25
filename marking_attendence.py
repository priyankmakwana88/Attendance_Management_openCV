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
#from add_student import add_student

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
	#READING STUDENT LIST
	roll=[]
	first_name=[]
	for i in values:
		if i[0] == 'ROLL NUMBER':
			continue
		else:
			roll.append(i[0])
			first_name.append(i[1])
	#print(roll)
	#print(first_name)
	
	#LOADING ENCODINGS OF THE STUDENT CURRENTLY IN CLASS
	count=face_in_class_live()
	current_class_encoding=[]
	for i in range(1,count+1):
		student = face_recognition.load_image_file("current_class/student"+str(i)+".jpeg")
		student_encoding = face_recognition.face_encodings(student)[0]	
		current_class_encoding.append(student_encoding)
	#print(current_class_encoding)
	#print(count)
	#print(len(current_class_encoding))

	
	#LOADING ENCODINGS OF ENROLLED STUDENT
	enrolled_face_encodings=[]
	enrolled_face_names=[]
	for i in range(1,len(roll)+1):
		enrolled = face_recognition.load_image_file("Students/"+str(roll[i-1])+"/5.jpeg") #loading 5th image for check
		enrolled_encoding = face_recognition.face_encodings(enrolled)[0]	
		enrolled_face_encodings.append(enrolled_encoding)
		enrolled_face_names.append(first_name)
	#print(enrolled_face_encodings)	---- list of array
	#print(enrolled_face_names)	---- list of list
	
	#COMPARING ENCODINGS
	present_today_roll=[]
	present_today_name=[]
	for i in range(0,len(current_class_encoding)):
		results = face_recognition.compare_faces(enrolled_face_encodings, current_class_encoding[i])
		print(results)
		#GETTING PRESENTEE NAME AND ROLL
		for j in range(0,len(results)):
			if results[j]==True:
				present_today_roll.append(roll[j])
				present_today_name.append(first_name[j])
				print(first_name[j]+' - '+str(roll[j])+' detected!')
	

	#MARKING IN REGISTER
	for i in range(1,len(roll)+1):
		if roll[i-1] in present_today_roll:
			excel.write(i,s.ncols,'P')
	
	#UNDETECTED FOLLOW-THROUGH
	undetected = count-len(present_today_roll)
	if undetected>0:
		print(str(undetected)+' left undetected, kindly enroll them or throw them out of the class!!')
		#to_enroll=input('\nShould i be a good boy and enroll them for you?? (y/n)')
		#if to_enroll == 'y' or to_enroll == 'Y':
		#	add_student()
		
	#COMITTING THE EDITS IN DATABASE
	edit_sheet.save('attendence_database.xls')

else:
	print("Attendence marked for today!!")



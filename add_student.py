#!/usr/bin/python3

#IMPORTING LIBRARIES
import face_recognition
import cv2
import numpy as np
from xlrd import open_workbook
from xlutils.copy import copy
import os
import time

#IMPORTING XML FILE
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascase = cv2.CascadeClassifier('haarcascade_eye.xml')

#INITIALIZING CAMERA
cam = cv2.VideoCapture(0)

#READ THE PRESENT DATABASE
#MAINTAINING DATABASE OF STUDENT PRESENT
workbook = open_workbook("database_student.xls")
workbook2= open_workbook("attendence_database.xls")

edit_sheet = copy(workbook)
edit_sheet2= copy(workbook2)

s=workbook.sheets()[0]
s2=workbook2.sheets()[0]

#READING XLS GLOBAL DB
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

#READING XLS ATTENDENCE DB
values2=[]
for row in range(s2.nrows):
	col_value = []
	for col in range(s2.ncols):
		value  = (s2.cell(row,col).value)
		try : value = str(int(value))
		except : pass
		col_value.append(value)
	values2.append(col_value)
#print (values2)


#CREATING STUDENT LIST BY ROLL NUMBER
roll=[]
first_name=[]
for i in values:
	if i[1] == 'ROLL NUMBER':
		continue
	else:
		roll.append(i[1])
		first_name.append(i[2])
print(roll)
print(first_name)


#PERFORMING AMBIGUITY CHECK
print('BE READY!!  Reading your face in \n3\n')
time.sleep(1)
print('2\n')
time.sleep(1)
print('1\n')
time.sleep(1)
status,check_img=cam.read()
cv2.imwrite('ambiguity_process/latest_suspect.jpeg',check_img)
#cam.release()
print('\n\nPLEASE WAIT while we perform ambiguity check ')


#READING SUSPECT
status='need_enrolement'
captured_picture = face_recognition.load_image_file("ambiguity_process/latest_suspect.jpeg")
captured_face_encoding = face_recognition.face_encodings(captured_picture)[0]
for i in range(0,len(roll)):
	student_picture = face_recognition.load_image_file("Students/"+roll[i]+"/5.jpeg")	  #READING 5th PICTURE OF PRESENT STUDENT
	student_face_encoding = face_recognition.face_encodings(student_picture)[0]		  #ENCODING THE PICTURE
	
	result = face_recognition.compare_faces([student_face_encoding], captured_face_encoding)  #GENERATING RESULT
	
	if result[0] == True:
		print("Don't try to be smart, you already have been enrolled as "+first_name[i])
		status='enrolled'
		break


if status == 'need_enrolement':

	#READING STUDENT INFORMATION
	s_fname=input("Enter student's first name : ")
	s_lname=input("Enter student's last name : ")
	s_roll_number=input("Enter student's roll number : ")
	
	


	#CHECKING COUNT IN DATABASE XLS
	if values[-1][0]=='Sno':	#EMPTY SHEET
		count=0
	else:				#FETCHING LAST SERIAL NUMBER
		count=int(values[-1][0])

	#WRITING NEW STUDENT INFORMATION IN GLOBAL XLS
	excel = edit_sheet.get_sheet(0)
	excel.write(count+1,0,count+1)
	excel.write(count+1,1,s_roll_number)
	excel.write(count+1,2,s_fname)
	excel.write(count+1,3,s_lname)

	#WRITING NEW STUDENT INFORMATION IN ATTENDANCE XLS
	excel2 = edit_sheet2.get_sheet(0)
	excel2.write(count+1,0,s_roll_number)
	excel2.write(count+1,1,s_fname)
	

	#SAVING THE STUDENT INTO DATABASE
	edit_sheet.save('database_student.xls')
	edit_sheet2.save('attendence_database.xls')

	os.system('mkdir Students/'+s_roll_number)
	
	#READING STUDENT IMAGE
	img_count=1
	while True:
		status,frame = cam.read()
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.1, 5)
		for (x, y, w, h) in faces:    
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
			roi_gray = gray[y:y+h,x:x+w]
			roi_color = frame[y:y+h,x:x+w]
			cv2.imwrite('Students/'+str(s_roll_number)+'/'+str(img_count)+'.jpeg',roi_color)
		img_count=img_count+1
		cv2.imshow('STUDENT',frame)	
		if cv2.waitKey(10) & img_count>12:
			break
	print('THANK YOU '+s_fname+', you have been added to the database.')
	cam.release()
	cv2.destroyAllWindows()

else:
	print('\nTHANK YOU FOR OUR WASTING TIME!')

#!/usr/bin/env python3

#IMPORTING LIBRARIES
import cv2
from xlrd import open_workbook
from xlutils.copy import copy
import face_recognition
import os
import datetime

#IMPORTING SELF-MADE FUNCTIONS
#from face_in_class_live import face_in_class_live
#from add_student import add_student

video_capture = cv2.VideoCapture(0)

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
	
		
	#LOADING ENCODINGS OF ENROLLED STUDENT
	enrolled_face_encodings=[]
	enrolled_face_names=[]
	enrolled_face_rolls=[]
	for i in range(1,len(roll)+1):
		enrolled = face_recognition.load_image_file("Students/"+str(roll[i-1])+"/7.jpeg") #loading 5th image for check
		enrolled_encoding = face_recognition.face_encodings(enrolled)[0]	
		enrolled_face_encodings.append(enrolled_encoding)
		enrolled_face_names.append(first_name[i-1])
		enrolled_face_rolls.append(roll[i-1])
	#print(enrolled_face_encodings)	---- list of array
	print(enrolled_face_names)#	---- list of list
	

	#
	# Initialize some variables
	face_locations = []
	face_encodings = []
	face_names = []
	process_this_frame = True
	present=[]
	while True:
	    
		# Grab a single frame of video
	    
		ret, frame = video_capture.read()
		# Resize frame of video to 1/4 size for faster face recognition processing
		small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
		# Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
		rgb_small_frame = small_frame[:, :, ::-1]
	
		# Only process every other frame of video to save time
		if process_this_frame:
			# Find all the faces and face encodings in the current frame of video
			face_locations = face_recognition.face_locations(rgb_small_frame)
			face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
	
			face_names = []
			for face_encoding in face_encodings:
				# See if the face is a match for the known face(s)
				matches = face_recognition.compare_faces(enrolled_face_encodings, face_encoding)
				name = "Unknown"
				# If a match was found in known_face_encodings, just use the first one.
				if True in matches:
					first_match_index = matches.index(True)
					name = enrolled_face_names[first_match_index]
					roll = enrolled_face_rolls[first_match_index]
					#name = f_name+'-'+str(roll)
				face_names.append(name)
	
		process_this_frame = not process_this_frame
		
		# Display the results
		for (top, right, bottom, left), name in zip(face_locations, face_names):
			# Scale back up face locations since the frame we detected in was scaled to 1/4 size
			top *= 4
			right *= 4
			bottom *= 4
			left *= 4
	
			# Draw a box around the face
			cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
			# Draw a label with a name below the face
			cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
			font = cv2.FONT_HERSHEY_DUPLEX
			#print(name)
	       
			cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
			if roll not in present:
				present.append(roll)
	
		# Display the resulting image
		cv2.imshow('Video', frame)
		# Hit 'q' on the keyboard to quit!
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	
	# Release handle to the webcam
	video_capture.release()
	cv2.destroyAllWindows()
	print (present)
	#
	
	
	#MARKING IN REGISTER
	
	for i in range(0,len(enrolled_face_rolls)):
		if enrolled_face_rolls[i] in present:
			excel.write(i+1,s.ncols,'P')
			print(enrolled_face_names[i]+' recognised.')
			
	#COMITTING THE EDITS IN DATABASE
	edit_sheet.save('attendence_database.xls')
	
else:
	print("Attendence marked for today!!")



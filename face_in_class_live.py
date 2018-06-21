#!/usr/bin/python3

#IMPORTING LIBRARIES
import face_recognition
import cv2

#GETTING CURRENT CLASS IMAGE
image_loc=input('Enter the current class image path : ')

#READING FACES OF STUDENT IN CLASS
image = face_recognition.load_image_file(image_loc)
face_locations = face_recognition.face_locations(image)

#print(face_locations)

#EXTRACTING FACE OF EACH STUDENT IN CLASS
count=0
for i in face_locations:
	print(i)
	count=count+1
	x1=i[0]
	x2=i[1]
	y2=i[2]
	y1=i[3]
	#print(x1,y1,x2,y2)
	face=image[y1:y2,x1:x2]
	cv2.imwrite('current_class/student'+str(count)+'.jpeg',face)
	
print('Total student present in class = '+str(count))


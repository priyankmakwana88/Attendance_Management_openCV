#!/usr/bin/python3

''' last update june23 - mak '''

#IMPORTING LIBRARIES
import face_recognition
import cv2

def face_in_class_live():
	#GETTING CURRENT CLASS IMAGE
	choice=input('Do you want to click live photo or wanna upload? (click/upload)')
	if choice=='upload':
		image_loc=input('Enter the current class image path : ')
		image = face_recognition.load_image_file(image_loc)
	else:
		cam=cv2.VideoCapture(0)
		image=cam.read()[1]	
		cv2.imwrite('hi.jpeg',image)
		cam.release()
	#READING FACES OF STUDENT IN CLASS
	face_locations = face_recognition.face_locations(image)
	
	#EXTRACTING FACE OF EACH STUDENT IN CLASS
	count=0
	for i in face_locations:
		print(i)
		count=count+1
		y1=i[0]	#top
		x2=i[1] #right
		y2=i[2] #bottom
		x1=i[3] #left
		#print(x1,y1,x2,y2)
		face=image[y1:y2,x1:x2]
		#print(face)
		cv2.imwrite('current_class/student'+str(count)+'.jpeg',face)
		
	print('Total student present in class = '+str(count))
	return count

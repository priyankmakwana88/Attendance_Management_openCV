#!/usr/bin/env python3

import face_recognition

picture_of_me = face_recognition.load_image_file("/home/priyank/Desktop/emma.jpeg")
my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

picture_of_me2 = face_recognition.load_image_file("Students/129/10.jpeg")
my_face_encoding2 = face_recognition.face_encodings(picture_of_me2)[0]
# my_face_encoding now contains a universal 'encoding' of my facial features that can be compared to any other picture of a face!

unknown_picture = face_recognition.load_image_file("chk.jpg")
unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

# Now we can see the two face encodings are of the same person with `compare_faces`!

results = face_recognition.compare_faces([my_face_encoding,my_face_encoding2], unknown_face_encoding)

#print(my_face_encoding)
print(results)
if results[0] == True:
    print("It's a picture of me!")
else:
    print("It's not a picture of me!")

#!/usr/bin/env python3


#IMPORTING LIBRARIES
import numpy as np
import matplotlib.pyplot as plt
from xlrd import open_workbook
from xlutils.copy import copy
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage                   
from email.mime.text import MIMEText
import os
import time
import smtplib
import getpass

#CREATING MAIL INSTANCE
msg=MIMEMultipart()

#ACCESSING DATABASE
workbook = open_workbook("attendence_database.xls")
edit_sheet = copy(workbook)
s=workbook.sheets()[0]
excel = edit_sheet.get_sheet(0)


workbook2 = open_workbook("database_student.xls")
edit_sheet2 = copy(workbook2)
s2=workbook2.sheets()[0]

#READING XLS GLOBAL DB
values_global = []
for row in range(s2.nrows):
	col_value = []
	for col in range(s2.ncols):
		value  = (s2.cell(row,col).value)
		try : value = str(int(value))
		except : pass
		col_value.append(value)
	values_global.append(col_value)
print(values_global)

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
#print(values)

#COPYING DB VALUES INTO PLACEHOLDER
new_values=[]
for i in values:
	new_values.append(i)


#REMOVING DATA LABELS
for i in range(0,len(new_values)):
	new_values[i]=new_values[i][2:]



#GETTING COLLOBRATIVE ATTENDENCE DATA
date_list=new_values[0]
present_datewise=[]
for i in range(0,len(new_values[0])):
	count=0
	for j in range(1,len(new_values)):
		if 'P' in new_values[j][i]:
			count=count+1
	present_datewise.append(count)

#PLOTTING VALUES  (DAYWISE OVERALL GRAPH)
plt.title('ATTENDANCE REPORT')
plt.xlabel('DATES')
plt.ylabel('CLASS STRENGTH')
plt.bar(date_list,present_datewise,color='r')
plt.show()


#GETTING PERSONAL ATTENDANCE DATA
count_attendence=[]
choice_use=input('Do you want to moniter invidual attendence of any individual student? (y/n)')
if choice_use=='y' or choice_use=='Y':
	individual_roll=input('Enter roll number of student whose attendence you want to moniter : ')
	for i in range(len(values)):
		if individual_roll==values[i][0]:
			individual_name=values[i][1]
			attendance_individual=values[i][2:]
			for j in attendance_individual:
				if j == 'P':	
					count_attendence.append('1')
				else:
					count_attendence.append('0')

	#PLOTTING VALUES  (DAYWISE PERSONAL GRAPH)
	plt.title('ATTENDANCE REPORT OF '+individual_name)
	plt.xlabel('DATES')
	plt.ylabel('STUDENT STRENGTH')
	plt.gca().invert_yaxis()
	plt.plot(date_list,count_attendence,color='r')
	plt.show()


#SEND MAIL ROLL NUMBER LIST (MAINTAIN 70%)
mail_list=[]
total_class=len(date_list)
for i in range(1,len(values)):
	total_present=0	
	for j in range(2,len(values[i])):
		if values[i][j]=='P':
			total_present=total_present+1
	percent_attendence=(total_present*100)/total_class
	if percent_attendence<70:
		mail_list.append(values[i][1])

mail_list_email=[]
for i in range(len(mail_list)):
	for j in range(len(values_global)):
		if mail_list[i] in values_global[j]:
			mail_list_email.append(values_global[j][-1])



#SENDING MAIL FOR MAIL-LIST
msg['From'] = str('projectnapster88@gmail.com')

# take password in secretive form
pswd = 'projectnapster@sys1'

for i in range(len(mail_list_email)):
	msg['To'] = str(mail_list_email[i])
	msg['Subject'] = str('Regarding low attendance!')

	message = 'Hello,\n\tThis is to inform you that your attendance is running low!\nPlease, specify the reason at the office else a strict action will be taken against you.\n\nThank You.'

	# connection establishment using smtp object   
	mail = smtplib.SMTP('smtp.gmail.com',587)
	mail.ehlo()
	mail.starttls()
	
	# login in the server
	mail.login(msg['From'],pswd)
	
	# send the mail to the receiver
	mail.sendmail(msg['From'],msg['To'],message)
mail.close()
	








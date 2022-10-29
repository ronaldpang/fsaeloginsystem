#i need to install pypng python library in order to scan the qr code ~~~~
#i need to import png library before running the file
#if the pc does not have a camera, then the code will not work
#need to fix the qr code line, it captures the generated qr code but it does not actually work
#also need to find a way to view the database sheet, the information that is being inputted in the python executable file
#turn this file into a totally executable file
#info of who is in a shop/

#;0125674161?


#TODO link python output to sync with MS Teams

#goal is to view the login file on teams and know who is in the shop
#ask tyler if he has his raspberry pi or find some in SDELC
#get the scanner thing from PARSA
#NEW THINGS/REQUIREMENTS TO MEET
#login & logout
#keep a record of how long the person has been in the shop in total
#microcontroller to scan ID. using the student id number recognizes.
#raspberry pi to run OS and scan
#student id number matches with the database
#instead of using database to output and view data, try excel sheet? and link that with one drive > teams

#libraries used: time, png, getpass, tqdm, sqlite3, pyzbar, pyqrcode, cv2, os, numpy, colorama
import time
import png
import getpass
from tqdm.auto import tqdm
import cv2
import os
import numpy
import colorama
from colorama import Back, Style
from csv import writer
import csv
import pandas as pd

colorama.init(autoreset=True)

#Function to scan Student ID card and read into scanner 
#------ScanningFromCardReader---------------------
def scan():#this reads the student id from the card reader
	studentid=input()
	studentid=santize(studentid)
	filename = 'FSAETEAMLEAD.csv'
	with open(filename, 'r' ) as csvfile:
		scanlist = list(csvfile)
		csvreader=csv.reader(csvfile)
		print(scanlist[1])
		# for row in scanlist:
			
		# 	print(scanlist)
    



#Creates a database file whenever input records are in place
#------CreateDatabaseForeEmployee------------------
# def database():
# 	conn = sqlite3.connect('FSAETEAMLEADDatabase.db')
# 	c = conn.cursor()
# 	c.execute("CREATE TABLE IF NOT EXISTS all_record(employee_name TEXT, employee_id TEXT, employee_contact, employee_department TEXT)")
# 	conn.commit()
# 	conn.close()
# database()

#Prompts user to input information
#------AddingNewUsers/Team Lead---------------------
#def add_User():
	#Li = []
	#E_name=str(input("Please Enter Team Lead Name\n"))
	#E_id=str(input("Please Enter Team Lead Id\n"))
	#E_contac= input("Please enter Team Lead Contact No\n")
	#E_dept= input("Please enter Team Lead Department\n")
	#Li.extend((E_name,E_id,E_contac,E_dept))
    #-----using List Comprehension to convert a list to str--------------
	#listToStr = ' '.join([str(elem) for elem in Li])
	#print(listToStr)
	#print(Back.YELLOW + "Please Verify the Information")
	#print("Employee Name       = "+ E_name)
	#print("Employee ID         = "+ E_id)
	#print("Employee Contact    = "+ E_contac)
	#print("Employee Department = "+ E_dept)
	#input("Press Enter to continue or CTRL+C to Break Operation")
	#conn = sqlite3.connect('FSAETEAMLEADDatabase.db')
	#c = conn.cursor()
	#c.execute("INSERT INTO all_record(employee_name, employee_id, employee_contact, employee_department) VALUES (?,?,?,?)", (E_name,E_id,E_contac,E_dept))
	#conn.commit()
	#qr= pyqrcode.create(listToStr)
	#if not os.path.exists('./QrCodes'):
	#	os.makedirs('./QRCodes')
	#qr.png("./QRCodes/" +E_name+ ".png",scale=8)

	
#------This funcion would convert studentid number that is being swiped into actual studentid number----	
def santize(E_id):
	santized = E_id
	santized = santized[2:11]
	return santized

def add_User():	
	Li = []
	E_name=str(input("Your Name: \n"))
	E_id=str(input("Please Swipe Your Student ID: \n"))
	E_id = santize(E_id)
	E_contac= input("Your Contact Phone Number: \n")
	E_dept= input("Your Team Position: \n")
	Li.extend((E_name,E_id,E_contac,E_dept))
    #-----using List Comprehension to convert a list to str--------------
	listToStr = ' '.join([str(elem) for elem in Li])
    #print(listToStr)
	print(Back.YELLOW + "Please Verify the Information")
	print("Name               = "+ E_name)
	print("Student ID         = "+ E_id)
	print("Phone Number       = "+ E_contac)
	print("Team Position      = "+ E_dept)
	input(Back.LIGHTRED_EX + "Press Enter to continue or CTRL+C to Break Operation")
	with open('FSAETEAMLEAD.csv','a')as adder:
		writer_object = writer(adder)
		writer_object.writerow(Li)
		adder.close()
    
#This function is used to create the 
#--------------ViewDataset------------------------
def viewdata():
	rows = []
	with open("FSAETEAMLEAD.csv", 'r') as file:
		csvreader=csv.reader(file)
		for row in csvreader:
			rows.append(row)
			print(row)
		# 	for printing in row:
		# 		print(printing)
	#print(header[0],header[1])
	#print(row[0], row[1])
    # read by default 1st sheet of an excel file
# 	conn = sqlite3.connect('FSAETEAMLEADDatabase.db')
# 	c = conn.cursor()
# 	c.execute('''CREATE TABLE IF NOT EXISTS Record(name TEXT, iid TEXT,phone_no TEXT, dept TEXT, TimeofMArk TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL )''') #creates the table in the database if it does not exist yet
# 	c.execute("SELECT * FROM Record")
# 	rows = c.fetchall()
# 	for row in rows:
# 		print(row)
# 	conn.close()
#----------AdminScreen-----------------------
def afterlogin():
	print("+------------------------------+")
	print("|  1- Add New Team Lead         |")
	print("|  2- View Record               |")
	print("+------------------------------+")
	user_input = input("")
	if user_input == '1':
		add_User()
	if user_input == '2':
		viewdata()
		

#Login--------------------------------------
def login():
	print(Back.CYAN+ 'Please Enter Password :')
	print(Back.YELLOW+"Student ID Attendance System")
	password = getpass.getpass()
	if password =='fsae':
		for i in tqdm(range(4000)):
			print("",end='\r')
		print("------------------------------------------------------------------------------------------------------------------------")
		print(Back.BLUE+"Card Swipe Attendance System: ")
		afterlogin()
	if password != 'fsae':
		print("Invalid Password")
		login()

#---Verifying User----
#def verifyuser():


#-------MainPage----------------------------
def markattendance():
	print("+------------------------------+")
	print("|  1- Mark Attendance          |")
	print("|  2- Admin Login              |")
	print("+------------------------------+")
	user_input2 = input("")
	if user_input2== '1':
		scan()
	if user_input2 == '2':
		login()
markattendance()

#create a function that will erase all created data entered into the excel sheet

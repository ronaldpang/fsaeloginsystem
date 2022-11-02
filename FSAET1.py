#TODO link python output to sync with MS Teams
#TODO implement the veriy user system
#TODO make an excel sheet with all of the team leads info
#TODO get the raspberry pi from john
#TODO swipe card once: login, swipe card twice:logout
#TODO function that will erase all data if user selects its



#-----libraries used: time, png, getpass, tqdm, sqlite3, pyzbar, pyqrcode, cv2, os, numpy, colorama----
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

	
#------This funcion would convert studentid number that is being swiped into actual studentid number----	
def santize(E_id):
	santized = E_id
	santized = santized[2:11]
	return santized


#----Adding user to the system-----
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
		

#----------Login---------------
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

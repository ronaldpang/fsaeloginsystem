#TODO implement the veriy user system
#TODO make an excel sheet with all of the team leads info
#TODO swipe card once: login, swipe card twice:logout
#TODO function that will erase all data if user selects its
#TODO function that allows user to navigate through the screen #DONE
#TODO implementation of the raspberry pi as a login system
#TODO rework the screenchoice() UI
#TODO make an excutable file that could run off of the raspberry pi
#TODO ensure that indents and spacing are all regular instead of tab spacing



#-----libraries used: time, png, getpass, tqdm, sqlite3, pyzbar, pyqrcode, cv2, os, numpy, colorama, pandas, numpy, re----
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
import numpy as np
colorama.init(autoreset=True)
import re

#------This funcion would convert studentid number that is being swiped into actual studentid number----	
def sanitize(E_id):
	# Perform regex match on ID string, ignoring characters
	re_sanitized = re.split(r'(1[0-9]{7})', E_id)
	
	# Search the list returned by regex.split for the ID string
	for item in re_sanitized:
		if len(item) == 8: # Student IDs are 8 digits long, 7 if indexed at 0
			re_sanitized = item
	# Type conversion to int
	re_sanitized = int(re_sanitized)
	return re_sanitized


#---Verifying User---- (TEST ME FIRST)
def verifyuser(userID: int, df_log: pd.DataFrame) -> pd.Series:
    isUser: bool = False
    for index,row in df_log.iterrows():
        if(row["ID"] == userID):
            userRow = pd.Series(row)
            return userRow
        else: 
            # User does not exist in log, so we prompt them to add themselves to it
		    # create user entry in log
	        # create series from newly created row (or vice versa)
            pass
            return userRow

# vvv These functions needs testing vvv
"""	
#---Check-In---
def checkIn(userID: int, userRow: pd.Series) -> pd.Series:
	if(userRow['Present:'] == "Present"):
		userRow['Present:'] = "Absent"
		userRow['Time Out:'] = time.now()
	else:
		userRow['Present:'] == "Present"
		userRow['Time In:'] = time.now()
	return userRow


#---Update Log---
def update_log(userRow: pd.Series, df_log: pd.DataFrame):
	for index, row in df_log:
		if(row["ID"] == userRow["ID"]):
			row = userRow
"""

#Function to scan Student ID card and read into scanner 
#------Build log DataFrame------------------------
def build_df(filename:str) -> pd.DataFrame:
	filename = 'FSAETEAMLEAD.csv'
	if(os.path.isfile(filename)):
		df_log = pd.read_csv(filename)
	return df_log

#------ScanningFromCardReader---------------------
def scan() -> None:#this reads the student id from the card reader
	studentid=input()
	studentid=sanitize(studentid)
	filename = 'FSAETEAMLEAD.csv'
	df_log = pd.read_csv(filename)
	verifyuser(studentid, df_log)

#----Adding user to the system-----
def add_User() -> None:	
	Li = []
	E_name=str(input("Your Name: \n"))
	E_id=str(input("Please Swipe Your Student ID: \n"))
	E_id = sanitize(E_id)
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
def viewdata() -> None:
	rows = []
	with open("FSAETEAMLEAD.csv", 'r') as file:
		csvreader=csv.reader(file)
		for row in csvreader:
			rows.append(row)
			print(row)
   
#----------AdminScreen-----------------------
def afterlogin() -> None:
    print("+------------------------------+")
    print("|  1- Add New Team Lead         |")
    print("|  2- View Record               |")
    print("+------------------------------+")
    user_input = input("")
    if user_input=='1':
        add_User()
    if user_input=='2':
        viewdata()
    while user_input != '1' or user_input != '2':
        user_input=input("Select either 1 or 2: ")
        if user_input == '1':
            add_User()
            break
        if user_input == '2':
            viewdata()
            break

#-----Screenchoice--------
def screenchoice() -> None:
    print("Press 1 to add another user: ")
    print("Press 2 to view the record again: ")
    user_input=input("Which screen would you like to go back to: ")
    if user_input=='1':
        add_User()
    if user_input=='2':
        viewdata()
    print("You will now be moved back to the home screen")
    

#----------Login---------------
def login() -> None:
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

#
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


# ------- Main Driver--------
if __name__ == "__main__":
    filename = 'FSAETEAMLEAD.csv'
    log = build_df(filename)
    print(log, '\n')
    markattendance()
    screenchoice()

# TODO link python output to sync with MS Teams
# TODO implement the veriy user system
# TODO make an excel sheet with all of the team leads info
# TODO get the raspberry pi from john
# TODO swipe card once: login, swipe card twice:logout
# TODO function that will erase all data if user selects its
# TODO function that allows user to navigate through the screen


# -----libraries used: time, png, getpass, tqdm, sqlite3, pyzbar, pyqrcode, cv2, os, numpy, colorama----
import datetime
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


# ------Build log DataFrame------------------------
def build_df(filename: str) -> pd.DataFrame:
    filename = "FSAETEAMLEAD.csv"
    if os.path.isfile(filename):
        df_log = pd.read_csv(filename)
    return df_log


# ------This funcion would convert studentid number that is being swiped into actual studentid number----
def santize(E_id):
    # Perform regex match on ID string, ignoring characters
    re_sanitized = re.split(r"(1[0-9]{7})", E_id)

    # Search the list returned by regex.split for the ID string
    for item in re_sanitized:
        if len(item) == 8:  # Student IDs are 8 digits long, 7 if indexed at 0
            re_sanitized = item
    # Type conversion to int
    re_sanitized = int(re_sanitized)
    return re_sanitized


# ------Locate User------------------------
def locate_user(userID: int, log: pd.DataFrame) -> pd.Series:
    try:
        return pd.Series(log.loc[userID])
    except KeyError:
        # Note to Ron - Error statements are placeholders; I plan on handling exceptions for an incorrect ID at some point
        print(
            "Specified ID is not in log. Please check if ID entered is correct, or add new user."
        )
        # retry here
        # else add new user


# ------Clock In------------------------
def clock_in(userID: int, log: pd.DataFrame) -> pd.DataFrame:
    curr_time = datetime.datetime.now()
    log.at[userID, "Time In"] = (
        str(curr_time.hour) + ":" + str(curr_time.minute) + ":" + str(curr_time.second)
    )
    log.at[userID, "Time Out"] = "None"
    log.at[userID, "Attendance"] = "Present"
    return log


# ------Clock Out------------------------
def clock_out(userID: int, log: pd.DataFrame) -> pd.DataFrame:
    curr_time = datetime.datetime.now()
    log.at[userID, "Time Out"] = (
        str(curr_time.hour) + ":" + str(curr_time.minute) + ":" + str(curr_time.second)
    )
    log.at[userID, "Attendance"] = "Absent"
    return log


# ------Add User------------------------
def add_user(log: pd.DataFrame) -> pd.DataFrame:
    userID: int = scan(log)
    # Note to Ron - These input statements are placeholders; feel free to replace with UX messages if you so choose
    userName: str = input("Please provide your First and Last name.")
    userNum: str = input("Please provide your phone number.")
    userTitle: str = input("Please provide your team title or role.")
    new_row = pd.Series(
        {
            "ID": int(userID),
            "Phone Num": userNum,
            "Name": userName,
            "Title": userTitle,
            "Time Entered": None,
            "Time Checkout": None,
            "Duration": None,
            "If Present": None,
        }
    )
    # Reset the two table's indexes before concatination
    log.reset_index(drop=False, inplace=True)
    # Combine
    log = pd.concat([log, new_row.to_frame().T], ignore_index=True)
    # Set ID column to type int
    log["ID"] = log["ID"].astype(int)
    # Set index to ID
    log.set_index("ID")

    return log


# ------Update name------------------------
def update_name(userID: int, log: pd.DataFrame) -> None:
    new_name: str = input("Please enter your new username.")
    log.loc[userID, "Name"] = new_name


# ------Update Number------------------------
def update_number(userID: int, log: pd.DataFrame) -> None:
    new_num: str = input("Please enter your new phone number.")
    log.loc[userID, "Phone Num"] = new_num


# ------Update Title------------------------
def update_title(userID: int, log: pd.DataFrame) -> None:
    new_title: str = input("Please enter your new title.")
    log.loc[userID, "Title"] = new_title


# ------Update Time------------------------
def update_time(userID: int, log: pd.DataFrame) -> None:
    time_format = "%I%M%p"  # %I = zero-padded hour, %M = zero-padded minute, and %p = AM or PM (I doubt people will know the second they walked in)
    arrival_time: str = input(
        "Please enter the time you arrived today, in 12-hour format with a leading zero (i.e. 09:05 AM)."
    )
    arrival_time_dt: datetime = datetime.strptime(arrival_time, time_format)
    log.loc[userID, "Time Entered"] = arrival_time_dt
    departure_time: str = input("Would you like to clock out now? (y/yes or n/no)")
    if departure_time.upper() == "Y" or departure_time.upper() == "YES":
        clock_out(userID, log)


# ------Erase User------------------------
def erase_user(userID: int, log: pd.DataFrame) -> None:
    confirm1: str = input(
        "Please type yes (or y) to confirm you would like to delete this user."
    )
    if confirm1.upper() == "YES" or confirm1.upper() == "Y":
        confirm2: str = input(
            "WARNING: You are about to delete a user from the log! Are you sure you want to do this?"
        )
        if confirm2.upper() == "YES" or confirm2.upper() == "Y":
            log.drop([userID], axis=0, inplace=True)


# ------ScanningFromCardReader---------------------
def scan(
    df_log: pd.DataFrame,
) -> None:  # this reads the student id from the card reader
    studentid = input()
    studentid = santize(studentid)
    filename = "FSAETEAMLEAD.csv"
    verifyuser(studentid, df_log)


# ----Adding user to the system-----
def add_User() -> None:
    Li = []
    E_name = str(input("Your Name: \n"))
    E_id = str(input("Please Swipe Your Student ID: \n"))
    E_id = santize(E_id)
    E_contac = input("Your Contact Phone Number: \n")
    E_dept = input("Your Team Position: \n")
    Li.extend((E_name, E_id, E_contac, E_dept))
    # -----using List Comprehension to convert a list to str--------------
    listToStr = " ".join([str(elem) for elem in Li])
    # print(listToStr)
    print(Back.YELLOW + "Please Verify the Information")
    print("Name               = " + E_name)
    print("Student ID         = " + E_id)
    print("Phone Number       = " + E_contac)
    print("Team Position      = " + E_dept)
    input(Back.LIGHTRED_EX + "Press Enter to continue or CTRL+C to Break Operation")
    with open("FSAETEAMLEAD.csv", "a") as adder:
        writer_object = writer(adder)
        writer_object.writerow(Li)
        adder.close()


# This function is used to create the data set
# --------------ViewDataset------------------------
def viewdata() -> None:
    rows = []
    with open("FSAETEAMLEAD.csv", "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            rows.append(row)
            print(row)


# ----------AdminScreen-----------------------
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


# -----Screenchoice--------
def screenchoice() -> None:
    print("Press 1 to add another user: ")
    print("Press 2 to view the record again: ")
    user_input = input("Which screen would you like to go back to: ")
    if user_input == "1":
        add_User()
    if user_input == "2":
        viewdata()
    print("You will now be moved back to the home screen")


# ----------Login---------------
def login() -> None:
    print(Back.CYAN + "Please Enter Password :")
    print(Back.YELLOW + "Student ID Attendance System")
    password = getpass.getpass()
    if password == "fsae":
        for i in tqdm(range(4000)):
            print("", end="\r")
        print(
            "------------------------------------------------------------------------------------------------------------------------"
        )
        print(Back.BLUE + "Card Swipe Attendance System: ")
        afterlogin()
    if password != "fsae":
        print("Invalid Password")
        login()


# -------MainPage----------------------------
def markattendance(df_log: pd.DataFrame):
    print("+------------------------------+")
    print("|  1- Mark Attendance          |")
    print("|  2- Admin Login              |")
    print("+------------------------------+")
    user_input2 = input("")
    if user_input2 == "1":
        scan(df_log)
    if user_input2 == "2":
        login()


# ------- Main Driver--------
if __name__ == "__main__":
    filename = "FSAETEAMLEAD.csv"
    log = build_df(filename)
    print(log, "\n")
    markattendance(log)
    screenchoice()

# ========================= JAKE TO DO LIST =========================
# TODO remove microseconds from the duration output
# TODO write clock_in / clock_out function, and update, infinitely
# TODO Rework main menu structure
# TODO function that allows user to navigate through the screen (go back if you select the wrong menu)
# TODO finish exception handling
#   TODO Finalize sanitize exception handling
<<<<<<< HEAD
=======
# TODO add admin menu to main_menu function
# TODO test update function edge cases
# TODO figure out a "lunch break" system (?)
# TODO import pycfg to view control flow graphs
>>>>>>> 0a2008785e6f8fc81944ac48142b7f2e5f87e0a5

# ========================= MAIN TO DO LIST =========================
# TODO link python output to sync with MS Teams
# TODO implement the veriy user system
# TODO make an excel sheet with all of the team leads info
# TODO get the raspberry pi from john
# TODO function that allows user to navigate through the screen

# ========================= DONE LIST =========================
# DONE swipe card once: login, swipe card twice:logout
# DONE function that will erase all data if user selects it
# DONE finalize documentation

# -----libraries used: time, png, getpass, tqdm, sqlite3, pyzbar, pyqrcode, cv2, os, numpy, colorama----
import datetime
import time
import png
import getpass
from tqdm.auto import tqdm

# import cv2
import os
import colorama
from colorama import Back, Style
from csv import writer
import csv
import pandas as pd
import numpy as np

colorama.init(autoreset=True)
import re
import sys


"""
# ------Build log DataFrame------------------------
Parameters: filename - the name, as string, of the csv file to be opened
Returns: a pandas DataFrame
Possible Errors: Dependent on the error caught during the reading of the file (possibly many)
Calls: pandas helpers, basic python
Description: Creates a pandas DataFrame object from the given csv file, and sets the index of the frame to the ID column
"""


def build_df(filename: str) -> pd.DataFrame:
    if os.path.isfile(filename):
        try:
            df_log = pd.read_csv(filename, on_bad_lines="error")
            df_log.set_index("ID", inplace=True)
        except:
            print(
                "ERROR! An exception occured while trying to read the csv file!",
                sys.exc_info[2],
            )
        return df_log
    else:
        print(
            "ERROR! File path to "
            + filename
            + " cannot be found! Program will now terminate."
        )
        sys.exit()


"""
# ------Locate User------------------------
Parameters: userID - the integer ID of the most recent card swipped; log - pandas DataFrame being altered
Returns: Series - the row of userID
Possible Errors: KeyError - missing ID, IndexingError - the index (ID) does not match the frame (log) index
Calls: pandas helpers, basic python
Description: Finds a specified user from the log and returns a series (row) with their information
"""


def locate_user(userID: int, log: pd.DataFrame) -> pd.Series:
    return pd.Series(log.loc[userID])


"""
# ------Get Attendance------------------------
Parameters: userID - the integer ID of the most recent card swipped; log - pandas DataFrame being altered
Returns: attendance data as a string
Possible Errors: KeyError - missing ID, IndexingError - the index (ID) does not match the frame (log) index
Calls: pandas helpers, basic python
Description: Finds a specified user from the log and returns a string with their attedance information
"""
def get_attendance(userID: int, df_log: pd.DataFrame) -> str:
    return str(df_log.at[userID, "If Present:"])


"""
# ------Clock In------------------------
Parameters: userID - the integer ID of the most recent card swipped; log - pandas DataFrame being altered
Returns: None
Possible Errors: KeyError - missing ID; ValueError - missing tuple [row, col]
Calls: pandas helpers, basic python
Description: Sets the specified user to 'Present' and clocks the time they swipped their card.
"""


def clock_in(userID: int, log: pd.DataFrame) -> None:
    curr_time = datetime.datetime.now()
    curr_time_str = curr_time.strftime("%Y-%m-%d %H:%M:%S")
    log.at[userID, "Time Entered:"] = curr_time_str
    log.at[userID, "Time Checkout:"] = np.nan
    log.at[userID, "If Present:"] = "Present"


"""
# ------Clock Out------------------------
Parameters: userID - the integer ID of the most recent card swipped; log - pandas DataFrame being altered
Returns: None
Possible Errors: KeyError - missing ID; ValueError - missing tuple [row, col]; DateTime shouldn't cause any errors due to its implementation
Calls: pandas helpers, datetime, basic python
Description:
"""


def clock_out(userID: int, log: pd.DataFrame) -> None:
    curr_time = datetime.datetime.now()
    curr_time_str = curr_time.strftime("%Y-%m-%d %H:%M:%S")
    log.at[userID, "Time Checkout:"] = curr_time_str
    log.at[userID, "If Present:"] = "Absent"
    time_difference = curr_time - datetime.datetime.strptime(log.at[userID, "Time Entered:"], "%Y-%m-%d %H:%M:%S")
    log.at[userID, "Duration:"] = str(time_difference)[:-7]


"""
# ------Add User------------------------
Parameters: log - pandas DataFrame being altered
Returns: DataFrame - the updated attendance log
Possible Errors: KeyError - missing ID; ValueError - missing tuple [row, col]; 
Calls: scan, pandas helpers, datetime, basic python
Description: Adds a new user to the log with their requested information, and fills the time logs with NaN values.
"""


def add_user(log: pd.DataFrame) -> pd.DataFrame:
    userID: int = scan(log)
    # Note to Ron - These input statements are placeholders; feel free to replace with UX messages if you so choose
    userName: str = input("Please provide your First and Last name.")
    userNum: str = input("Please provide your phone number.")
    userTitle: str = input("Please provide your team title or role.")
    # Measure current time
    curr_time = datetime.datetime.now()
    curr_time = curr_time.strftime("%Y-%m-%d %H:%M:%S")
    # Fill in new row with info
    new_row = pd.Series(
        {
            "ID": int(userID),
            "Phone Num": userNum,
            "Name": userName,
            "Title": userTitle,
            "Time Entered:": curr_time,
            "Time Checkout:": np.nan,
            "Duration:": np.nan,
            "If Present:": "Present",
        }
    )
    # Reset the two table's indexes before concatination
    log.reset_index(drop=False, inplace=True)
    # Combine
    log = pd.concat([log, new_row.to_frame().T], ignore_index=True)
    # Set ID column to type int
    log["ID"] = log["ID"].astype(int)
    # Set index to ID
    log = log.set_index("ID")

    return log


"""
# ------Update name------------------------
Parameters: userID - the integer ID of the most recent card swipped; log - pandas DataFrame being altered
Returns: None
Possible Errors: KeyError - missing ID; ValueError - missing tuple [row, col]
Calls: pandas helpers, basic python
Description: Updates the name of a scanned ID.
"""


def update_name(userID: int, log: pd.DataFrame) -> None:
    new_name: str = input("Please enter your new username.")
    log.loc[userID, "Name"] = new_name


"""
# ------Update Number------------------------
Parameters: userID - the integer ID of the most recent card swipped; log - pandas DataFrame being altered
Returns: None
Possible Errors: KeyError - missing ID; IndexingError - the index (ID) does not match the frame (log) index
Calls: pandas helpers, basic python
Description: Updates the phone number of the specified user
"""


def update_number(userID: int, log: pd.DataFrame) -> None:
    new_num: str = input("Please enter your new phone number.")
    log.loc[userID, "Phone Num"] = new_num


"""
# ------Update Title------------------------
Parameters: userID - the integer ID of the most recent card swipped; log - pandas DataFrame being altered
Returns: None
Possible Errors: KeyError - missing ID; IndexingError - the index (ID) does not match the frame (log) index
Calls: pandas helpers, basic python
Description: Updates the team title of the specified user
"""


def update_title(userID: int, log: pd.DataFrame) -> None:
    new_title: str = input("Please enter your new title.")
    log.loc[userID, "Title"] = new_title


"""
# ------Erase User------------------------
Parameters: userID - the integer ID of the most recent card swipped; log - pandas DataFrame being altered
Returns: None
Possible Errors: KeyError - missing ID
Calls: pandas helpers, basic python
Description: Asks for confirmation, twice, before erasing a user from the log
"""


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


"""
# ------ScanningFromCardReader---------------------
Parameters: df_log - pandas DataFrame being altered
Returns: studentid - the scanned ID number as an integer
Possible Errors: None (?)
Calls: sanitize, pandas helpers, basic python
Description: Takes a scanned ID card, pulls the ID number, and 'sanitizes' it by removing junk values using RegEx
"""


def scan(df_log: pd.DataFrame) -> int:
    studentid = input("Please scan your student ID card now.")
    studentid = santize(studentid)
    return studentid


"""
# ------This funcion would convert studentid number that is being swiped into actual studentid number----
Parameters: E_id - string containing the student ID number passed by scan function
Returns: re_sanitized - the student ID number as an integer
Possible Errors: N/A - The regex match will simply fail
Calls: re, basic python
Description: parse the scanned ID string using RegEx to match the ID number without the junk data, and return it as an integer
"""


def santize(E_id: str) -> int:
    # Perform regex match on ID string, ignoring characters
    re_sanitized = re.split(r"(1[0-9]{7})", E_id)
    if re_sanitized == None:
<<<<<<< HEAD
        re_sanitized = input("ID extraction failed, please enter your student ID by tpying the numbers here:")
    else: # Search the list returned by regex.split for the ID string
        for item in re_sanitized:
            if len(item) == 8:  # Student IDs are 8 digits long, 7 if indexed at 0
                re_sanitized = item
        # Type conversion to int
=======
        pass
    # Search the list returned by regex.split for the ID string
    for item in re_sanitized:
        if len(item) == 8:  # Student IDs are 8 digits long, 7 if indexed at 0
            re_sanitized = item
    # Type conversion to int
>>>>>>> 0a2008785e6f8fc81944ac48142b7f2e5f87e0a5
    re_sanitized = int(re_sanitized)
    return re_sanitized

"""
# ----------Login---------------
Parameters: None
Returns: None
Possible Errors: TODO
Calls: Basic Python, getpass
Description: Admin login system which grants access to admin functions like erase_user and update_[user_field]
"""
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

"""
# --------------ViewDataset------------------------
"""
def viewdata() -> None:
    rows = []
    with open("FSAETEAMLEAD.csv", "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            rows.append(row)
            print(row)

"""
# ----------AdminScreen-----------------------
"""
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


"""
# ------Menu Diver---------------------
Parameters: None
Returns: None
Possible Errors: Many - exception handling should catch the glaring ones that the individual functions aren't designed to catch themselves
Calls: pandas helpers, basic python, all above functions
Description: Main driver for the punch clock, this function should run infinitely, or until the admin closes the program
"""
<<<<<<< HEAD
def main_menu() -> None: # TODO Restructure menu
    filename: str = "FSAETEAMLEAD.csv"
    attendance_log = build_df(filename)
    menu_input: str = input("Would you like to start the punch clock? (y/yes or n/no)")
    if menu_input.upper() == "Y" or menu_input.upper() == "YES":
        while True:
            print("+------------------------------+")
            print("|  1- Mark Attendance          |")
            print("|  2- Admin Login              |")
            print("+------------------------------+")
            menu_input = input("Enter 1 or 2 for menu options, and enter x to close the system.")
            if menu_input == "1":
                try:
                    user_ID = scan(attendance_log)
                except KeyError:
                    error_handler: str = input(
                        "This user is not entered into the system, would you like to add this user? (y/yes or n/no)"
                    )
                    if error_handler.upper() == "Y" or error_handler.upper() == "YES":
                        add_User(userID, attendance_log)
                    else:  # What should we do if the user thinks they're in the system but it returns a KeyError?
                        pass
                except ValueError:
                    print(
                        "An indexing error has occured. Either the specified ID is not an index for a user, or the indexing scheme has been altered. Please contact the system admin."
                    )
                    sys.exit()
                if(get_attendance(user_ID, attendance_log).upper() == "PRESENT"):
                    clock_out(user_ID, attendance_log)
                else:
                    clock_in(user_ID, attendance_log)
                print(attendance_log)
            if menu_input == "2":
                login()
            if menu_input.upper() == "X":
                sys.exit()
            # Clear previous user data from variables
            userID = np.Inf
    else:
        sys.exit() # Need to rework menu flow, this is placeholder
=======


def main_menu() -> None:
    filename: str = "FSAETEAMLEAD.csv"
    attendance_log = build_df(filename)
    start: str = input("Would you like to start the punch clock? (y/yes or n/no)")
    if start.upper() == "Y" or start.upper() == "YES":
        while True:
            userID = scan(attendance_log)
            specified_user = None
            try:
                specified_user = locate_user(userID, attendance_log)
            except KeyError:
                error_handler: str = input(
                    "This user is not entered into the system, would you like to add this user? (y/yes or n/no)"
                )
                if error_handler.upper() == "Y" or error_handler.upper() == "YES":
                    add_User(userID, attendance_log)
                else:  # What should we do if the user thinks they're in the system but it returns a KeyError?
                    pass
            except ValueError:
                print(
                    "An indexing error has occured. Either the specified ID is not an index for a user, or the indexing has been altered. Please contact the system admin."
                )
                # TODO Should we quit if this error occurs, or handle it and continue running?
            if specified_user["If Present:"] == "Absent":
                clock_in(userID, attendance_log)
            else:
                clock_out(userID, attendance_log)

            # Clear previous user data from variables
            userID = np.Inf
            specified_user = None
    else:  # TODO The rest of the menu occurs here (i.e. admin functions, erasing/updating users, etc.)
        pass
>>>>>>> 0a2008785e6f8fc81944ac48142b7f2e5f87e0a5


# ------Test Driver------------------------
if __name__ == "__main__":
    
    """
    # --------------------Test history--------------------
    # locate_user test
    print(locate_user(12526038, test_log))
    # clock_in and clock_out tests
    print(divider)
    test_log = clock_in(12526038, test_log)
    print(test_log)
    time.sleep(5)
    test_log = clock_out(12526038, test_log)
    print(test_log)
    print(divider)
    # Update user functions
    update_name(12526038, test_log)
    update_number(12526038, test_log)
    update_title(12526038, test_log)
    print(test_log)
    print(divider)
    # Erase_user test
    erase_user(12569902, test_log)
    print(test_log)
    print(divider)
    # Add_user test
    test_log = add_user(test_log)
    print(test_log)
    print(divider)
    """
    main_menu()
    

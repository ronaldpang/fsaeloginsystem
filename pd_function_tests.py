# ========================= JAKE TO DO LIST =========================
# TODO make punch clock run infinitely / Rework main menu structure
# TODO sync csv to onedrive
# TODO function that allows user to navigate through the screen (go back if you select the wrong menu)
# TODO finish exception handling
#   TODO Finalize sanitize exception handling

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
                sys.exc_info()[2],
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
Parameters: userID - the integer ID of the most recent card swipped; df_log- pandas DataFrame being altered
Returns: Series - the row of userID
Possible Errors: KeyError - missing ID, IndexingError - the index (ID) does not match the frame (log) index
Calls: pandas helpers, basic python
Description: Finds a specified user from the df_logand returns a series (row) with their information
"""


def locate_user(userID: int, df_log: pd.DataFrame) -> pd.Series:
    return pd.Series(df_log.loc[userID])


"""
# ------Get Attendance------------------------
Parameters: userID - the integer ID of the most recent card swipped; df_log- pandas DataFrame being altered
Returns: attendance data as a string
Possible Errors: KeyError - missing ID, IndexingError - the index (ID) does not match the frame (log) index
Calls: pandas helpers, basic python
Description: Finds a specified user from the log and returns a string with their attedance information
"""


def get_attendance(userID: int, df_log: pd.DataFrame) -> str:
    return str(df_log.at[userID, "If Present:"])


"""
# ------Clock In------------------------
Parameters: userID - the integer ID of the most recent card swipped; df_log- pandas DataFrame being altered
Returns: None
Possible Errors: KeyError - missing ID; ValueError - missing tuple [row, col]
Calls: pandas helpers, basic python
Description: Sets the specified user to 'Present' and clocks the time they swipped their card.
"""


def clock_in(userID: int, df_log: pd.DataFrame) -> None:
    curr_time = datetime.datetime.now()
    curr_time_str = curr_time.strftime("%Y-%m-%d %H:%M:%S")
    df_log.at[userID, "Time Entered:"] = curr_time_str
    df_log.at[userID, "Time Checkout:"] = np.nan
    df_log.at[userID, "If Present:"] = "Present"


"""
# ------Clock Out------------------------
Parameters: userID - the integer ID of the most recent card swipped; df_log- pandas DataFrame being altered
Returns: None
Possible Errors: KeyError - missing ID; ValueError - missing tuple [row, col]; DateTime shouldn't cause any errors due to its implementation
Calls: pandas helpers, datetime, basic python
Description:
"""


def clock_out(userID: int, df_log: pd.DataFrame) -> None:
    curr_time = datetime.datetime.now()
    curr_time_str = curr_time.strftime("%Y-%m-%d %H:%M:%S")
    df_log.at[userID, "Time Checkout:"] = curr_time_str
    df_log.at[userID, "If Present:"] = "Absent"
    time_difference = curr_time - datetime.datetime.strptime(
        df_log.at[userID, "Time Entered:"], "%Y-%m-%d %H:%M:%S"
    )
    df_log.at[userID, "Duration:"] = str(time_difference)[:-7]


"""
# ------Add User------------------------
Parameters: df_log- pandas DataFrame being altered
Returns: DataFrame - the updated attendance log
Possible Errors: KeyError - missing ID; ValueError - missing tuple [row, col]; 
Calls: scan, pandas helpers, datetime, basic python
Description: Adds a new user to the log with their requested information, and fills the time logs with NaN values.
"""


def add_user(df_log: pd.DataFrame) -> pd.DataFrame:
    userID: int = scan(df_log)
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
    df_log.reset_index(drop=False, inplace=True)
    # Combine
    df_log = pd.concat([df_log, new_row.to_frame().T], ignore_index=True)
    # Set ID column to type int
    df_log["ID"] = df_log["ID"].astype(int)
    # Set index to ID
    df_log = df_log.set_index("ID")

    return df_log


"""
# ------Update name------------------------
Parameters: userID - the integer ID of the most recent card swipped; df_log- pandas DataFrame being altered
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
Parameters: userID - the integer ID of the most recent card swipped; df_log- pandas DataFrame being altered
Returns: None
Possible Errors: KeyError - missing ID; IndexingError - the index (ID) does not match the frame (log) index
Calls: pandas helpers, basic python
Description: Updates the phone number of the specified user
"""


def update_number(userID: int, df_log: pd.DataFrame) -> None:
    new_num: str = input("Please enter your new phone number.")
    df_log.loc[userID, "Phone Num"] = new_num


"""
# ------Update Title------------------------
Parameters: userID - the integer ID of the most recent card swipped; df_log- pandas DataFrame being altered
Returns: None
Possible Errors: KeyError - missing ID; IndexingError - the index (ID) does not match the frame (log) index
Calls: pandas helpers, basic python
Description: Updates the team title of the specified user
"""


def update_title(userID: int, df_log: pd.DataFrame) -> None:
    new_title: str = input("Please enter your new title.")
    df_log.loc[userID, "Title"] = new_title


"""
# ------Update Time In------------------------
Parameters: userID - the integer ID of the most recent card swipped; df_log- pandas DataFrame being altered
Returns: None
Possible Errors: KeyError - missing ID; IndexingError - the index (ID) does not match the frame (log) index
Calls: pandas helpers, basic python
Description: Updates the time entered of the specified user
"""
def update_time_in(userID: int, df_log: pd.DataFrame) -> None:
    time_string: str = input("Please enter your new check-in time, in the following format: HH:MM:SS (i.e. 09:03:01 for 9:03am).")
    new_time_dt = datetime.datetime.strptime(time_string, "H%:M%:S%")
    df_log.loc[userID, "Time Entered:"] = new_time_dt.strftime("H%:M%:S%")
    if(df_log.loc[userID, "If Present:"] != "Present"):
        df_log.loc[userID, "If Present:"] = "Present"


"""
# ------Update Time In------------------------
Parameters: userID - the integer ID of the most recent card swipped; df_log- pandas DataFrame being altered
Returns: None
Possible Errors: KeyError - missing ID; IndexingError - the index (ID) does not match the frame (log) index
Calls: pandas helpers, basic python
Description: Updates the time entered of the specified user
"""
def update_time_out(userID: int, df_log: pd.DataFrame) -> None:
    time_string: str = input("Please enter your new check-out time, in the following format: HH:MM:SS (i.e. 09:03:01 for 9:03am).")
    new_time_dt = datetime.datetime.strptime(time_string, "H%:M%:S%")
    df_log.loc[userID, "Time Checkout:"] = new_time_dt.strftime("H%:M%:S%")
    df_log.loc[userID, "Duration:"] = datetime.datetime.strptime(df_log.loc[userID, "Time Entered:"], "H%:M%:S%") - new_time_dt
    if(df_log.loc[userID, "If Present:"] != "Absent"):
        df_log.loc[userID, "If Present:"] = "Absent" 


"""
# ------Update User------------------------
Parameters: userID - the integer ID of the most recent card swipped; df_log- pandas DataFrame being altered
Returns: None
Possible Errors: KeyError - missing ID; IndexingError - the index (ID) does not match the frame (log) index
Calls: pandas helpers, basic python
Description: Asks the user what field they would like to update for the given userID, then asks for the updated info from user
"""
def update_user(user_ID: int, df_log: pd.DataFrame) -> None:
    print("+-------------------------------+")
    print("|  1- Phone Number              |")
    print("|  2- Name                      |")
    print("|  3- Title                     |")
    print("|  4- Time In                   |")
    print("|  5- Time Out                  |")
    print("|  b- back to admin menu        |")
    print("+-------------------------------+")
    update_input:str = input("What field of user:" + str(user_ID) + " would you like to update? Please choose 1,2,3,4,5, or b.")
    while update_input.upper() != "B":
        if update_input.upper() == "1":
            update_number(user_ID, df_log)
        if update_input.upper() == "2":
            update_name(user_ID, df_log)
        if update_input.upper() == "3":
            update_title(user_ID, df_log)
        if update_input.upper() == "4":
            update_time_in(user_ID, df_log)
        if update_input.upper() == "5":
            update_time_out(user_ID, df_log)
        update_input = ""


"""
# ------Erase User------------------------
Parameters: userID - the integer ID of the most recent card swipped; df_log- pandas DataFrame being altered
Returns: None
Possible Errors: KeyError - missing ID
Calls: pandas helpers, basic python
Description: Asks for confirmation, twice, before erasing a user from the log
"""


def erase_user(userID: int, df_log: pd.DataFrame) -> None:
    confirm1: str = input(
        "Please type yes (or y) to confirm you would like to delete this user."
    )
    if confirm1.upper() == "YES" or confirm1.upper() == "Y":
        confirm2: str = input(
            "WARNING: You are about to delete a user from the df_log! Are you sure you want to do this?"
        )
        if confirm2.upper() == "YES" or confirm2.upper() == "Y":
            df_log.drop([userID], axis=0, inplace=True)


"""
# ------ScanningFromCardReader---------------------
Parameters: df_log - pandas DataFrame being altered
Returns: studentid - the scanned ID number as an integer
Possible Errors: None (?)
Calls: sanitize, pandas helpers, basic python
Description: Takes a scanned ID card, pulls the ID number, and 'sanitizes' it by removing junk values using RegEx
"""


def scan(df_log: pd.DataFrame) -> int:
    studentid = input(
        "Please scan your student ID card now, or type STOP to halt the punch clock program."
    )
    if studentid.upper() == "STOP":
        return -999
    else:
        studentid = santize(studentid)
    return studentid


"""
# ------Sanitize---------------------
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
        re_sanitized = input(
            "ID extraction failed, please enter your student ID by tpying the numbers here:"
        )
    else:  # Search the list returned by regex.split for the ID string
        for item in re_sanitized:
            if len(item) == 8:
                re_sanitized = item
    # Type conversion to int
    re_sanitized = int(re_sanitized)
    return re_sanitized


"""
# ----------Login---------------
Parameters: df_log - pandas DataFrame being altered
Returns: None
Possible Errors: TODO
Calls: Basic Python, getpass
Description: Admin login system which grants access to admin functions like erase_user and update_[user_field]
"""


def login(df_log: pd.DataFrame) -> None:
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
        admin_menu(df_log)
    if password != "fsae":
        print("Invalid Password")
        login(df_log)


"""
# ----------AdminScreen-----------------------
Parameters: df_log - pandas DataFrame being altered
"""


def admin_menu(df_log: pd.DataFrame) -> None:
    user_input: str = ""
    while user_input.upper() != "B":
        print("+-------------------------------+")
        print("|  1- View Logs                 |")
        print("|  2- Sync Logs                 |")
        print("|  3- Add New User              |")
        print("|  4- Erase User                |")
        print("|  5- Update Existing User      |")
        print("|  b- back to Main Menu         |")
        print("+-------------------------------+")
        user_input = input("Please select an option from the menu above. Enter 1,2,3,4,5, or b.")
        if user_input.upper() == "1":
            log_input = input("Would you like to view the current program log (1) or the last system log (2)?")
            if log_input.upper() == "1":
                view_DataFrame(df_log)
            if log_input.upper() == "2":
                view_csv()
        if user_input.upper() == "2":
            pass
        if user_input.upper() == "3":
            df_log = add_user(df_log)
        if user_input.upper() == "4":
            erase_ID = scan(df_log)
            try:
                erase_user(df_log)
            except KeyError:
                print("The specified user cannot be deleted as their ID was not found in the current program log.")
            except ValueError:
                print("An error has occurred relating to the indexing scheme of the log. Please contact the system admin.")
                sys.exit()
        if user_input.upper() == "5":
            update_ID = scan(df_log)
            update_user(update_ID, df_log)
            """
            try:
                
            except KeyError:
                print("The specified user cannot be updated as their ID was not found in the current program log.")
            except ValueError:
                print("An error has occurred relating to the indexing scheme of the log. Please contact the system admin.")
                sys.exit()
            """
        if user_input.upper() == "B":
            break
            
"""
# --------------view_DataFrame------------------------
"""


def view_DataFrame(df_log: pd.DataFrame) -> None:
    print(df_log)


"""
# --------------view_csvset------------------------
"""


def view_csv() -> None:
    rows = []
    with open("FSAETEAMLEAD.csv", "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            rows.append(row)
            print(row)


"""
# ---------- Resync Log-----------------------
"""


def resync_log():
    print(
        "This function currently does nothing. It will soon resync the df_logto OneDrive."
    )


"""
# ------Attendance Loop---------------------
Parameters: df_log - pandas DataFrame being altered
Returns: None
Possible Errors: KeyError - A user does not exist in the system and needs to be added; ValueError - a serious error has occured to the indexing scheme
Calls: Pandas Helpers, basic python, scan, get_attendance clock_in, and clock_out
"""


def attendance_loop(df_log: pd.DataFrame) -> None:
    while True:
        user_ID = scan(df_log)
        # Stop the infinite attendance logging loop to allow for admin login or program termination
        if (
            user_ID == -999
        ):  # -999 marks a sentinel integer that scan() passes up if a user types STOP instead of scanning an ID
            stop_command = input(
                "Would you like to enter the admin menu (A), or exit the program (X)?"
            )
            if stop_command.upper() == "A":
                login(df_log)
            if stop_command.upper() == "X":
                sys.exit()
            break
        try:
            # Mark user's attendance in the log
            if get_attendance(user_ID, df_log).upper() == "PRESENT":
                clock_out(user_ID, df_log)
            else:
                clock_in(user_ID, df_log)
        except KeyError:
            print(
                "This user is not entered into the system. Please contact the system admin."
            )
            # TODO add ability for user to scan card, add themself (without entering name, title, etc), and clock them in
            break
        except ValueError:
            print(
                "An indexing error has occured. Either the specified ID is not an index for a user, or the indexing scheme has been altered. Please contact the system admin."
            )
            break


"""
# ------Menu Diver---------------------
Parameters: None
Returns: None
Possible Errors: Many - exception handling should catch the glaring ones that the individual functions aren't designed to catch themselves
Calls: pandas helpers, basic python, all above functions
Description: Main driver for the punch clock, this function should run infinitely, or until the admin closes the program
"""


def main_menu() -> None:
    filename: str = "FSAETEAMLEAD.csv"
    attendance_log = build_df(filename)
    print("+------------------------------+")
    print("|  1- Admin Login              |")
    print("|  2- Start Punchclock         |")
    print("|  x- Close Program            |")
    print("+------------------------------+")
    menu_input = input(
        "Enter 1 or 2 for menu options, and enter x to close the system."
    )
    while menu_input.upper() != "X":
        if menu_input == "1":
            login(attendance_log)
        elif menu_input == "2":
            attendance_loop(attendance_log)
        elif menu_input.upper() == "X":
            sys.exit()
        else:
            menu_input = input("Please enter either a 1, 2, or x.")


# ------Test Driver------------------------
if __name__ == "__main__":
    divider="==============================================="
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
    """
    
    
    main_menu()

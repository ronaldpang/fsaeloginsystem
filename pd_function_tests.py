# ========================= JAKE TO DO LIST =========================
# TODO add exception handling in main
# TODO remove days from the duration output
# TODO test update function edge cases

# ========================= MAIN TO DO LIST =========================
# TODO link python output to sync with MS Teams
# TODO implement the veriy user system
# TODO make an excel sheet with all of the team leads info
# TODO get the raspberry pi from john
# TODO function that will erase all data if user selects its
# TODO function that allows user to navigate through the screen

##========================= DONE LIST =========================
# DONE swipe card once: login, swipe card twice:logout

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

# ------Build log DataFrame------------------------
def build_df(filename: str) -> pd.DataFrame:
    if os.path.isfile(filename):
        df_log = pd.read_csv(filename)
    df_log.set_index("ID", inplace=True)
    return df_log


# ------Locate User------------------------
def locate_user(userID: int, log: pd.DataFrame) -> pd.Series:
    return pd.Series(log.loc[userID])


# ------Clock In------------------------
def clock_in(userID: int, log: pd.DataFrame) -> None:
    curr_time = datetime.datetime.now()
    log.at[userID, "Time Entered:"] = curr_time
    log.at[userID, "Time Checkout:"] = np.nan
    log.at[userID, "If Present:"] = "Present"


# ------Clock Out------------------------
def clock_out(userID: int, log: pd.DataFrame) -> None:
    curr_time = datetime.datetime.now()
    log.at[userID, "Time Checkout:"] = curr_time
    log.at[userID, "If Present:"] = "Absent"
    # This bit is boken
    time_difference = curr_time - log.at[userID, "Time Entered:"]
    log.at[userID, "Duration:"] = time_difference


# ------Add User------------------------
def add_user(log: pd.DataFrame) -> pd.DataFrame:
    userID: int = scan(log)
    # Note to Ron - These input statements are placeholders; feel free to replace with UX messages if you so choose
    userName: str = input("Please provide your First and Last name.")
    userNum: str = input("Please provide your phone number.")
    userTitle: str = input("Please provide your team title or role.")
    # Measure current time
    curr_time = datetime.datetime.now()
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
def scan(df_log: pd.DataFrame) -> int:
    studentid = input("Please scan your student ID card now.")
    studentid = santize(studentid)
    return studentid


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


# ------Test Driver------------------------
if __name__ == "__main__":
    divider = "==============================================================="
    filename = "FSAETEAMLEAD.csv"
    test_log = build_df(filename)
    print(test_log)
    print(divider)
    """
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
    """
    # Add_user test
    test_log = add_user(test_log)
    print(test_log)
    print(divider)
    clock_out(12563998, test_log)
    print(test_log)
    print(divider)

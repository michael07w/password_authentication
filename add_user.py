import hashlib
import sqlite3
from sqlite3 import Error
from getpass import getpass
from setup_db import create_connection

def check_username(username):
    """Checks if username exists.

    Args:
        username (str): Username to be checked.

    Returns:
        boolean: True if username already exists in users table. Else, False.
    """
    # create database connection
    conn = create_connection("ppab6.db")

    # get usernames
    cur = conn.cursor()
    cur.execute("SELECT username FROM users WHERE username = (?)", (username,))
    users_with_username = len(cur.fetchall())

    # close connection
    conn.close()

    if users_with_username > 0:
        return True
    else:
        return False



def get_username():
    """Returns username entered by user.

    Returns:
        str: Username entered by user.
    """
    taken = True
    while taken == True:
        username = input("Please enter desired username: ")
        taken = check_username(username)
        if taken:
            print("Username already taken. Try again.")

    return username



def get_password_hash():
    """Returns hash of password entered by user.

    Returns:
        str: Hash of password entered by user.
    """
    password = getpass("Please enter desired password: ")
    password_bytestr = password.encode("utf-8")
    password_hashed = hashlib.sha256(password_bytestr).hexdigest()

    return password_hashed



def save_user(login_creds):
    """Adds username/password_hash to database.

    Args:
        username (str): Username to be stored.
        password_hash (str): Password hash to be stored.
    """
    # create database connection
    conn = create_connection("ppab6.db")

    # add username/password_hash to users table
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", login_creds)
    conn.commit()

    # close connection
    conn.close()



def add_user():
    # get username/password hash
    username = get_username()
    password_hash = get_password_hash()
    credentials = (username, password_hash)

    # save user to database
    save_user(credentials)

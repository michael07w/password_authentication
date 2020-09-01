import hashlib
import json
import add_user
import setup_db
from getpass import getpass

def login():
    """Prompts user for login credentials, then checks against database of valid creds.
    """
    # get database name from options.cfg
    db_name = setup_db.read_db()

    # get username/password from user
    username = input("Please enter username: ")
    password = getpass("Please enter password: ")

    # validate credentials
    if is_valid_credentials(username, password, db_name):
        print("Congrats, you've logged in!")



#
def is_valid_credentials(uname, pwd, db_name):
    """Checks user-entered credentials against database of user creds.

    Args:
        uname (str): Username entered by user.
        pwd (str): Password entered by user.
        db_name(str): Name of database file that stores valid user creds.

    Returns:
        (bool): True if both username and password are valid.
    """
    # Hash password entered by user
    pwd_bytestr = pwd.encode("utf-8")
    pwd_hashed = hashlib.sha256(pwd_bytestr).hexdigest()

    # validate credentials in database
    conn = setup_db.create_connection(db_name)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(1) FROM users WHERE username = (?)", (uname,))
    result_username = cur.fetchone()
    if result_username[0] == 0:
        print("Get Lost")
        return False
    else:
        # validate password
        cur.execute("SELECT password_hash FROM users WHERE username = (?)", (uname,))
        result_hash = cur.fetchone()
        if pwd_hashed != result_hash[0]:
            print("Get Lost")
            return False

    conn.close()

    return True



def get_choice():
    """Returns user's choice to login, add a user, or exit.

    Returns:
        (str): User's selection.
    """
    choice = input("""Please make a selection (1, 2, or 3):
    1) Login
    2) Add User
    3) Exit
    """)

    return choice



def main():
    choice = get_choice()

    while choice != '3':
        if choice == '1':
            login()
        elif choice == '2':
            add_user.add_user()
        choice = get_choice()

    exit(1)



if __name__ == '__main__':
    main()

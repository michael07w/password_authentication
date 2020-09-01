import hashlib
import json
import setup_db
from getpass import getpass

def main():
    # get database name from options.cfg
    db_name = setup_db.read_db()

    # get username/password from user
    username = input("Please enter username: ")
    password = getpass("Please enter password: ")

    # validate credentials
    if is_valid_credentials(username, password, db_name):
        print("Congrats, you've logged in!")



# Checks user-entered credentials against the dict of possible creds
def is_valid_credentials(uname, pwd, db_name):
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



if __name__ == '__main__':
    main()

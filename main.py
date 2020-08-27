import hashlib
import json

def main():
    # read config file with creds
    with open("creds.json") as f:
        creds = json.load(f)

    # organize user creds into dict where key,value is username,password
    user_creds = {}
    for user in creds:
        uname = user["username"]
        pwd = user["password"].encode("utf-8")
        user_creds[uname] = hashlib.sha256(pwd).hexdigest()

    # get username/password from user
    username = input("Please enter username: ")
    password = input("Please enter password: ")

    if is_valid_credentials(username, password, user_creds):
        print("My deepest darkest secret!")



# Checks user-entered credentials against the dict of possible creds
def is_valid_credentials(uname, pwd, creds):
    # Hash password entered by user
    pwd_bytestr = pwd.encode("utf-8")
    pwd_hashed = hashlib.sha256(pwd_bytestr).hexdigest()

    # validate credentials
    if uname not in creds:
        print("Get Lost")
        return False
    elif pwd_hashed != creds.get(uname):
        print("Get Lost")
        return False

    return True



if __name__ == '__main__':
    main()

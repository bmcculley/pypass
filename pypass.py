#!/usr/bin/env python
# a terrible way to store passwords using python and sqlite
#
# author Blake McCulley
# https://github.com/bmcculley/pypass
import base64 as b64
import sys
import sqlite3
import getpass

total = len(sys.argv)

cmdargs = sys.argv

# functions to encrypt or decrypt passwords
# need some fixing up
def encrypt(pswd):
    return b64.b64encode(pswd)

def decrypt(pswd):
    return b64.b64decode(pswd)

# function to interact with the database
# expects at least 2 arguements, a key for storing or fetching a password
# action for either adding or getting a password
# and istr where istr is the password for adding
def dbstor(ikey, action, istr = None):
    con = sqlite3.connect("pswd.db")
    c = con.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS passwords
                (key text, pswd text)''')
    if action == "add":
        c.execute("INSERT INTO passwords VALUES ('%s', '%s')" \
                    % (ikey, istr))
        con.commit()
        con.close()
        return True
    elif action == "get":
        c.execute("SELECT pswd FROM passwords WHERE key = '%s'" \
                    % ikey)
        return c.fetchone()[0]
    elif action == "update":
        c.execute("UPDATE passwords SET pswd = '%s' WHERE key = '%s'" \
            % (istr, ikey))
        con.commit()
        con.close()
        return True
    con.close()

if total > 1:
    passNext = False
    for n, item in enumerate(cmdargs):
        if n == 0 or passNext:
            pass
        elif item == "add":
            ikey = cmdargs[n+1]
            ipass = encrypt(getpass.getpass("Password: "))
            if dbstor(ikey, "add", ipass):
                print "Password successfully added to the database"
            else:
                print "An error occurred, password not saved."
            passNext = True
        elif item == "get":
            ikey = cmdargs[n+1]
            pswd = decrypt(dbstor(ikey, "get"))
            print pswd 
            passNext = True
        elif item == "update":
            ikey = cmdargs[n+1]
            ipass = encrypt(getpass.getpass("Password: "))
            if dbstor(ikey, "update", ipass):
                print "Password successfully updated in the database"
            else:
                print "An error occurred, password not updated."
            passNext = True
        else:
            print "Unknown arguement"
else:
    print "To add a password use:"
    print "pypass.py add <password key>"
    print "To retrieve a password use:"
    print "pypass.py get <password key>"
    print "To update a password use:"
    print "pypass.py update <password key>"

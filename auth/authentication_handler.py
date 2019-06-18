#!/usr/bin/env python3

# Author: Lauren Brown
# Program Name: JIRA Workflow Tools
# @created: 5/28/2019
# @modified: 6/5/2019
#

import os
import tempfile

from cryptography.fernet import Fernet
from pip._vendor.distlib.compat import raw_input
from colorama import init, Fore
from getpass import getpass

"""
#################################
####### Get the username ########
#################################
"""


def get_user():
    init()
    username = raw_input(Fore.CYAN + '>> Username: ')
    type(username)
    return username


"""
#################################
#### Cryptography Encryption ####
#################################
"""


def get_pwd():
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    # If not running in debug mode, then you should uncomment this
    # password = raw_input(Fore.CYAN + '>> Password: ')
    # type(password)

    # Note: Getpass only works on the console and debugging via IDE
    password = getpass(prompt=Fore.CYAN + '>> Password: ')

    pwd_to_encrypt = str.encode(password)
    ciphered_text = cipher_suite.encrypt(pwd_to_encrypt)  # required to be in bytes format

    try:
        fd, tmpfile = tempfile.mkstemp()
        file_ = os.fdopen(fd, "w+b")
        file_.write(ciphered_text)
        file_.seek(0)

        # Ensure the file is read/writable by the creator only
        saved_umask = os.umask(0o077)

    except IOError as error:
        print('An error occurred while writing the file: ' + error)

    finally:
        encrypted_file = (file_.read())  # The read contents of our saved file
        os.umask(saved_umask)
        file_.close()
        os.unlink(tmpfile)
        uncipher_text = (cipher_suite.decrypt(encrypted_file))
        plain_text_encryptedpassword = bytes(uncipher_text).decode("utf-8")  # convert to string

        return plain_text_encryptedpassword


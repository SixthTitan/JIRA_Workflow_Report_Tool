#!/usr/bin/env python3

# Author: Lauren Brown
# Program Name: JIRA Workflow Tools
# @created: 5/28/2019
# @modified: 6/5/2019
#

from jira import JIRA, JIRAError
from jira_interface.admin.config.config import *

"""
#########################
#### Initialize JIRA ####
#########################
"""


def jira_session(username, password):
    try:
        session = JIRA(options=options, auth=(username, password))
        return session
    except JIRAError as e:
        if e.status_code == 401:
            return print("Login to JIRA failed. Check your username and password")
        else:
            return print("Error:" + e.status_code, e.text)  # Todo: add additional custom error status messages

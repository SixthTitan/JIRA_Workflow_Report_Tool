#!/usr/bin/env python3

# Author: Lauren Brown
# Program Name: JIRA Workflow Tools
# @created: 5/28/2019
# @modified: 6/5/2019
#

"""
################################
#### JIRA Settings ####
################################
"""

# Project: name of the JIRA project to track
# Board: name of the Board to track
# Server: JIRA Base Server URL
# Async: Should REST requests be performed asynchronously?
# Async_Workers: The number of workers performing this async request (If enabled)
# Max Retries: The maximum amount of attempt's to make when the first REST Request fails, until it should give up
# Timeout: The maximum amount of time to wait on connecting to the JIRA Server before giving up
# HTML Output: The directory and filename of the generated html file for embedding into Confluence, this should be
# generated inside an Apache or Ngnix path
# Check_Update: should we check for a new version of the Python JIRA API when running requests?

options = {
    'project': '',  # Name of the JIRA Project to Track
    'sprint': '',  # Board Name to track
    'server': '',  # JIRA Base Server URL
    'confluence-host': "",  # Confluence Server Hostname
    'confluence-user': "",  # Confluence Username
    'confluence-pass': "",  # Confluence Password
    'async': True,  # Should REST requests be performed asynchronously?
    'async_workers': 5,
    'max_retries': 3,
    'timeout': 30,
    'page-id': "",  # ID of the space page in Confluence to upload attachments to
    'created-label': "# Open Issues Created",
    'updated-label': "# Open Issues Updated",
    "updated-file": "render/data/recent_updated_issues.json",
    "created-file": "render/data/recent_created_issues.json",
    "epic-file": "render/data/recent_story_epic.json",
    "image-name-updated": "updated.png",
    "image-name-created": "created.png",
    "output-dir": "render/output/",
    "graph-width": 0.5,
    "created_graph-color": "#BD2848",
    "updated_graph-color": "#006699",
    'check_update': False
}


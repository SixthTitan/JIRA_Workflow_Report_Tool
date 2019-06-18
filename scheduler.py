#!/usr/bin/env python3

# Author: Lauren Brown
# Program Name: JIRA Workflow Tools
# @created: 5/28/2019
# @modified: 6/5/2019
#

from jira_interface.admin.auth.session_handler import jira_session, JIRAError
from jira_interface.admin.auth.authentication_handler import get_user, get_pwd
from jira_interface.admin.render.generate_graph import generate_graph
from jira_interface.admin.render.embed_confluence import pre_load_files
from jira_interface.admin.config.config import *

from pyfiglet import Figlet
from colorama import Fore
from datetime import datetime, timedelta
from console_logging.console import Console

import schedule
import time
import platform
import os
import json

# @todo: implement uploading json file to confluence with embed confluence.py and then automatically delete
# @todo: the file after x days
# @todo: Look into implementing a way to create a new directory to store the image and html files
# @todo: see if it's possible to add job id's to track and log for job queue

console = Console()


def get_recent_epic():

    total_epic = 0
    new_issues = {}

    now = datetime.now()
    week_ago = now - timedelta(days=7)

    """
    #################################################################
    #### Search for new story epics since last week from today   ####
    #################################################################
    """

    try:
        issues = jira.search_issues('project=' + options['project'], startAt=0, maxResults=0, validate_query=True)

        # Get the total amount of Updated Open Issues today
        for new_issue in issues:
            if str(new_issue.fields.customfield_11201) >= str(week_ago):
                total_epic += 1
                new_issues[str(now.date())] = total_epic

    finally:
        with open("render/data/recent_story_epic.json", "a") as story_epic:
            json.dump(new_issues, story_epic)
            story_epic.write("\n")
            story_epic.close()


"""
############################################################
#### Get Recently Created Issues within the last 24h    ####
############################################################
"""


def get_recent_created():

    total_new_issues = 0
    new_issues = {}

    now = datetime.now()

    """
    ############################################################
    #### Search for new issues within the last 24 hours     ####
    ############################################################
    """

    try:
        issues = jira.search_issues('project=' + options['project'], startAt=0, maxResults=0, validate_query=True)

        # Get the total amount of Updated Open Issues today
        for new_issue in issues:
            if str(new_issue.fields.status) == 'Open' and str(new_issue.fields.created) >= str(now):
                total_new_issues += 1
                new_issues[str(now.date())] = total_new_issues

    finally:
        with open(options['created-file'], "a") as recent_created:
            json.dump(new_issues, recent_created)
            recent_created.write("\n")
            recent_created.close()

    """
    ############################################################
    #### Get Recently Updated Issues within the last 24h    ####
    ############################################################
    """


def get_recent_updated():

    total_new_issues = 0
    new_issues = {}

    now = datetime.now()

    """
    ############################################################
    #### Search for new issues within the last 24 hours     ####
    ############################################################
    """

    try:
        issues = jira.search_issues('project=' + options['project'], startAt=0, maxResults=0, validate_query=True)

        # Get the total amount of Updated Open Issues today
        for new_issue in issues:
            if str(new_issue.fields.status) == 'Open' and str(new_issue.fields.updated) >= str(now):
                total_new_issues += 1
                new_issues[str(now.date())] = total_new_issues

    finally:
        with open(options['updated-file'], "a") as recent_updated:
            json.dump(new_issues, recent_updated)
            recent_updated.write("\n")
            recent_updated.close()

    """
    ###################################################################
    #### Execute scheduled jobs and display current job queue      ####
    ###################################################################
    """


def job_board():

    # Clear the Console each time a job has been run to keep things nice and pretty
    if platform.system() == "Windows":
        os.system('cls')  # For Windows
    if platform.system() == "Linux" or platform.system() == "Darwin":
        os.system('clear')  # For Linux/OS X

    # Get the time from the last job that was executed and the time of the next scheduled run
    console.info(Fore.LIGHTCYAN_EX + "\n Scheduled Jobs: " + str(schedule.jobs) + "\n")


def pre_run_jobs():
    pre_load_files()  # Upload the files before attaching them to HTML as a link


def scheduled_jobs():
    job_board()  # Get our job queue and show window

    # Notify the user that the scheduled job is running now
    console.info(Fore.LIGHTGREEN_EX + '\n Running Scheduled Jobs, please wait... \n')

    # Add functions that should be run periodically here
    get_recent_updated()  # Get the total updated issues in the last 24 hours
    get_recent_created()  # Get the total created issues in the last 24 hours
    # get_recent_epic()  # Get the total story epics in the last week (Not fully implemented
    # and not able to return all of the epics
    generate_graph()  # Run our graph generator tool to make us the HTML and image files with our data


"""
######################################
#### Setup and Run Scheduled Jobs ####
######################################
"""

msg = Figlet(font='slant')
print(msg.renderText('JIRA Workflow'))


try:
    jira = jira_session(get_user(), get_pwd())  # Start a new JIRA Session
    jira.async_do(options['async_workers'])

except JIRAError as error:
    console.error(Fore.LIGHTRED_EX + "An error occurred while logging into JIRA: \n" +
                  error.status_code + "\n" +
                  error.response
                  )

finally:
    # Run scheduled jobs every Tuesday and Thursday at 7AM
    schedule.every().monday.at("06:50").do(pre_run_jobs)
    schedule.every().monday.at("07:00").do(scheduled_jobs)

    schedule.every().friday.at("06:50").do(pre_run_jobs)
    schedule.every().friday.at("07:00").do(scheduled_jobs)

    # Enable this if doing testing and or development
    # schedule.every(1).minutes.do(pre_run_jobs)
    # schedule.every(2).minutes.do(scheduled_jobs)

    while True:
        schedule.run_pending()
        time.sleep(1)


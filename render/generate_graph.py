#!/usr/bin/env python3

# Author: Lauren Brown
# Program Name: JIRA Workflow Tools
# @created: 5/28/2019
# @modified: 6/5/2019
#

from jira_interface.admin.config.config import *
from jira_interface.admin.render.embed_confluence import generate_content

from bokeh.plotting import figure
from bokeh.io import export_png, saving
from bokeh.layouts import gridplot
from bokeh.resources import Resources
from datetime import datetime
from console_logging.console import Console

import json
import pathlib

"""
######################################
#### DO NOT RUN THIS FILE DIRECTLY ###
######################################
"""

# IO File Handling
current_dir = pathlib.Path(__file__).parent

# For Recently Created Graph
total_created_issues = []
x = []
y = []

# For Recently Updated Graph
total_updated_issues = []
x1 = []
y1 = []

# Image Date
now = datetime.now().date()

console = Console()

resource = Resources
save_resource = resource(mode='cdn')


def generate_graph():
    """
        ######################################################
        #### Generate a graph for recently created issues ####
        ######################################################
    """

    # File Read Operations
    with open(options['created-file'], 'r') as issues_file:
        for line in issues_file:
            total_created_issues.append(json.loads(line))

    for data in total_created_issues:
        for time, amount in data.items():
            x.append(time)
            y.append(amount)

    graph = figure()

    # x is date
    x_line = str(x)

    # y is number of issues
    y_line = str(y)

    # Determine the maximum value
    maximum = max(y)

    graph.line(x_line, y_line, line_width=1)

    # vbar
    recent_created = figure(y_axis_label=options['created-label'], x_range=x, y_range=(0, maximum))
    recent_created.vbar(x=x, top=y, width=options['graph-width'], color=options['created_graph-color'],
                        legend=options['created-label'], line_dash="solid")
    export_png(recent_created, filename=options['output-dir'] + str(now) + "-" + options['image-name-created'])

    # line
    recent_created_line = figure(y_axis_label=options['created-label'], x_range=x, y_range=(0, maximum))
    recent_created_line.line(x=x, y=y, color=options['created_graph-color'], legend=options['created-label'])
    export_png(recent_created_line, filename=options['output-dir'] + str(now) + "-" + "line" + options['image-name-created'])

    # circle
    recent_created_circle = figure(y_axis_label=options['created-label'], x_range=x, y_range=(0, maximum))
    recent_created_circle.circle(x=x1, y=y1, color=options['created_graph-color'], legend=options['created-label'])
    export_png(recent_created_circle, filename=options['output-dir'] + str(now) + "-" + "circle" + options['image-name-created'])

    """
        ######################################################
        #### Generate a graph for recently updated issues ####
        ######################################################
    """
    # File Read Operations
    with open(options['updated-file'], 'r') as issues_file:
        for line in issues_file:
            total_updated_issues.append(json.loads(line))

    for data in total_updated_issues:
        for time, amount in data.items():
            x1.append(time)
            y1.append(amount)

    graph = figure()

    # x is date
    x_line = str(x1)

    # y is number of issues
    y_line = str(y1)

    # Determine the maximum value
    maximum = max(y1)

    graph.line(x_line, y_line, line_width=1)

    # vbar
    recent_updated = figure(y_axis_label=options['updated-label'], x_range=x1, y_range=(0, maximum))
    recent_updated.vbar(x=x1, top=y1, width=options['graph-width'], color=options['updated_graph-color'],
                        legend=options['updated-label'], line_dash="solid")
    export_png(recent_updated, filename=options['output-dir'] + str(now) + "-" + options['image-name-updated'])

    # line
    recent_updated_line = figure(y_axis_label=options['updated-label'], x_range=x1, y_range=(0, maximum))
    recent_updated_line.line(x=x1, y=y1, color=options['updated_graph-color'], legend=options['updated-label'])
    export_png(recent_updated_line, filename=options['output-dir'] + str(now) + "-" + "line" + options['image-name-updated'])

    # circle
    recent_updated_circle = figure(y_axis_label=options['updated-label'], x_range=x1, y_range=(0, maximum))
    recent_updated_circle.circle(x=x1, y=y1, color=options['updated_graph-color'], legend=options['updated-label'])
    export_png(recent_updated_circle, filename=options['output-dir'] + str(now) + "-" + "circle" + options['image-name-updated'])

    """
    ###############################################################
    #### Generate and save an HTML view to embed to Confluence ####
    ###############################################################
    """

    saving.save(gridplot([recent_created, recent_updated, recent_created_line, recent_updated_line,
                          recent_created_circle, recent_updated_circle],
                         ncols=3, sizing_mode="scale_width", plot_height=300, plot_width=300),
                title="JIRA Workflow Metrics - " + str(now),
                filename=options['output-dir'] + str(now) + ".html", resources=save_resource)

    # Now upload the new HTML report to confluence
    generate_content()


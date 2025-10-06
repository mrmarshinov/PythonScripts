#!/usr/bin/env python3
import subprocess as sub
import sys

# Set your target workspace here starting from 1
try:
    target_workspace = int(sys.argv[1])
except IndexError:
    target_workspace = 2
# Read you previous workspace
try:
    with open("current.txt", "r") as f:
        previous_workspace = int(f.read())
except FileNotFoundError:
    previous_workspace = 1

# Checking opened workspaces
workspaces = sub.check_output(["wmctrl","-d"], text=True)
workspace_list = workspaces.strip().split("\n")
number_of_workspaces = len(workspace_list)

# Create target workspace if it necessary
if target_workspace > number_of_workspaces:
    sub.run(["wmctrl","-n",f"{target_workspace}"])

# Check current workspace
for i, workspace in enumerate(workspace_list):
    if "*" in workspace:
        current_workspace = i + 1

# Switch to target workspace if needed or switch to previous
if current_workspace != target_workspace:
    sub.run(['wmctrl',"-s", f"{target_workspace - 1}"])
    with open("current.txt", "w") as f:
        f.write(f"{current_workspace}")
else:
    sub.run(['wmctrl', "-s", f"{previous_workspace - 1}"])

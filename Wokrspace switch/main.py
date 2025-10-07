#!/usr/bin/env python3
import subprocess as sub
import sys
import json

#Read settings
try:
    with open("workspace_setting.json", "r", encoding='utf-8') as f:
        settings = json.load(f)
except FileNotFoundError:
    settings = {"previous_workspace": 1, "target_workspace": 2}

#Read target workspace from arguments
try:
    sys_target_workspace = int(sys.argv[1])
except (IndexError, ValueError):
    sys_target_workspace = 2

if sys_target_workspace < 2 or sys_target_workspace > 20:
    settings["target_workspace"] = 2
else:
    settings["target_workspace"] = sys_target_workspace

#Check opened workspaces
workspaces = sub.check_output(["wmctrl", "-d"], text=True)
workspace_list = workspaces.strip().split("\n")
number_of_workspaces = len(workspace_list)

#Create target workspace if necessary
if settings["target_workspace"] > number_of_workspaces:
    sub.run(["wmctrl", "-n", str(settings["target_workspace"])])

#Find current workspace
for i, workspace in enumerate(workspace_list):
    if "*" in workspace:
        current_workspace = i + 1
        break
else:
    current_workspace = 1

#Switch workspaces
if current_workspace != settings["target_workspace"]:
    settings["previous_workspace"] = current_workspace
    sub.run(["wmctrl", "-s", str(settings["target_workspace"] - 1)])
else:
    sub.run(["wmctrl", "-s", str(settings["previous_workspace"] - 1)])

#Save settings
with open("workspace_setting.json", "w", encoding='utf-8') as f:
    json.dump(settings, f, ensure_ascii=False, indent=4)

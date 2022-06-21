#
# Copyright 2022, Patryk Bełzak
#
# This file is part of Gotify alerts.
# Gotify alerts is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Gotify alerts is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Gotify alerts. If not, see <https://www.gnu.org/licenses/>.
# 
# Simple check to lookup free space on device and send notification to gotify

import os
import sys
import socket
import requests
import argparse

#####
# HANDLE HELP AND ARGUMENTS
parser = argparse.ArgumentParser(prog='check_disk.py', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
# REQUIRED ARGS
parser.add_argument('-t', '--token', help='your gotify token', type=str, required=True)	# non positional arguments
parser.add_argument('-U', '--URL', help='your gotify URL', type=str, required=True)
parser.add_argument('-w', '--warn', help='warn level, can be either size or %% depending on chosen format', type=int, default=10, required=True)
parser.add_argument('filesystem', type=str, nargs='+')	# positional arguments, allow to grab more than one arg and iterate over them
# OPTIONAL ARGS
parser.add_argument('-u', '--unit', help='unit size', type=str, default="GB")
parser.add_argument('-b', '--bytes', help='set size format for warnings rather than percent', action="store_true")
parser.add_argument('--hostname', help='insert your own host name instead of grabbed from host itself', type=str)
parser.add_argument('-p', '--priority', help='set gotify message priority', type=int, default=5)
args = parser.parse_args()

# calculates free blocks and total blocks on filesystem
def check_space(path):
    global free_blocks, total_blocks
    statvfs = os.statvfs(path)
    free_blocks = statvfs.f_frsize * statvfs.f_bfree
    total_blocks = statvfs.f_blocks * statvfs.f_frsize

# converts filesystem blocks to human readable format
def calc_space():
    for fs in args.filesystem:
        check_space(fs)
        # skip unit conversion if you want to have percents as result:
        if not args.bytes:
            freespace[fs] = free_blocks
            totalspace[fs] = total_blocks
        # or convert as desired
        elif args.unit == "MB":
            freespace[fs] = round(free_blocks / 1024 / 1024 , 2)
            totalspace[fs] = round(total_blocks / 1024 / 1024 , 2)
        elif args.unit == "GB":
            freespace[fs] = round(free_blocks / 1024 / 1024 / 1024, 2)
            totalspace[fs] = round(total_blocks / 1024 / 1024 / 1024, 2)
        elif args.unit == "TB":
            freespace[fs] = round(free_blocks / 1024 / 1024 / 1024 / 1024, 2)
            totalspace[fs] = round(total_blocks / 1024 / 1024 / 1024 / 1024, 2)
        else:
            sys.exit("ERROR:\nUnit [-u] has to be one of: MB, GB, TB")

# checks for unit format and sends alert to gotify
def send_alert():
    if args.hostname:
        hostname = args.hostname
    else:
        hostname = socket.gethostname()
    token = args.token
    URL = args.URL + "/message?token=" + token
    if args.bytes:
        for fs, free in freespace.items():
            message = fs + " has " + free + " " +  args.unit + " free space"
            data = {'title': "WARNING: " + hostname + " filesystem " + " is almost full",
                    'priority': args.priority,
                    'message': str(message)}
            if free < args.warn:
                r = requests.post(url = URL, data = data)
    else:
        if args.warn not in range(100):
            sys.exit("ERROR:\nWarn percent [-w] value must be integer between 0-100")
        for key in freespace.keys():
            freepct = freespace[key] / totalspace[key] * 100
            message = key + " has " + str(round(freepct, 1)) + "% free space"
            data = {'title': "WARNING: " + hostname + " filesystem " + " is almost full",
                    'priority': args.priority,
                    'message': message}
            if freepct < args.warn:
                r = requests.post(url = URL, data = data)

freespace = {}
totalspace = {}

def main():
    calc_space()
    send_alert()

main()


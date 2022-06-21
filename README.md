# Gotify checks
Standalone system/service checks that pushes alerts to gotify.
## Getting started
Clone repository to your local machine using `git clone`.
### Prerequisites
`python 3` is must have, follow you OS instructions for installation method.
Any `cron` would be nice to have, as you have to schedule checks somehow.
`pip3` is needed for installation of missing modules (see below).
`requests` is python module that most likely isn't available in clean python3 installation. It's used in every script to send notifications.
Please follow https://docs.python.org/3/installing/index.html for instructions on how to install modules or just execute `python -m pip install requests`.

### Usage
#### Check_disks
```
~ python checks/check_disk.py -h
usage: check_disk.py [-h] -t TOKEN -U URL -w WARN [-u UNIT] [-b]
                     [--hostname HOSTNAME] [-p PRIORITY]
                     filesystem [filesystem ...]

positional arguments:
  filesystem

options:
  -h, --help            show this help message and exit
  -t TOKEN, --token TOKEN
                        your gotify token (default: None)
  -U URL, --URL URL     your gotify URL (default: None)
  -w WARN, --warn WARN  warn level, can be either size or % depending on
                        chosen format (default: 10)
  -u UNIT, --unit UNIT  unit size (default: GB)
  -b, --bytes           set size format for warnings rather than percent
                        (default: False)
  --hostname HOSTNAME   insert your own host name instead of grabbed from
                        host itself (default: None)
  -p PRIORITY, --priority PRIORITY
                        set gotify message priority (default: 5)
```
## What's next
Work in progress:
* check_updates
To do:
* Check RAM
* Check CPU
* Check service
* Check website endpoint
Ideas?
 
## Project goal
I realize that these checks may not solve any existing problem, as there are plenty of grown and established monitoring solutions (like nagios or zabbix) that may send notifications to gotify.
Still, I have few arguments why actually I'm writing it:
1. I want to learn python by doing
2. I couldn't make nagios talk to my gotify server, also I got scared to break production monitoring, and too lazy to make dev environment.
3. I need monitoring solution without root priviliges.
4. I want to monitor with it only mission critical hosts/services

## Contributing
Any help or advice is highly aprreciated.

## License
This project is licensed under the GPL License - see the [COPYING](COPYING) file for details


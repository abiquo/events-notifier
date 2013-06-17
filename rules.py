#!/usr/bin/env python

#       The Abiquo Platform
#       Cloud management application for hybrid clouds
#       Copyright (C) 2008-2013 - Abiquo Holding S.L. 
#
#       This application is free software; you can redistribute it and/or
#       modify it under the terms of the GNU LESSER GENERAL PUBLIC
#       LICENSE as published by the Free Software Foundation under
#       version 3 of the License
#
#       This software is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#       LESSER GENERAL PUBLIC LICENSE v.3 for more details.
#
#       You should have received a copy of the GNU Lesser General Public
#       License along with this library; if not, write to the
#       Free Software Foundation, Inc., 59 Temple Place - Suite 330,
#       Boston, MA 02111-1307, USA.

import threading
import os.path, time
import datetime

def clear_rule_list():
    global rule_list
    rule_list = []

# Helper function that helps determinate if rules.cfg file has been modified
def last_rule_modification(date_time):
    global rule_modification_ts
    # Check if variable has been initialized
    try: rule_modification_ts
    # If not, set first modification timestamp and return true to force first rule load
    except NameError: 
        rule_modification_ts = date_time
        return True
    # If it exist, check if file has been modified since last execution
    else:
        if rule_modification_ts == date_time:
            return False
        else:
            rule_modification_ts = date_time
            return True 
  
def add_rule(rule):
    rule_list.append(rule)

def get_rule_list():
    return rule_list

def update_rule_list():
    # rule_update() is called every 60 seconds

    try:
        # Check if rules.cfg file has been modified
        reload_rules = last_rule_modification(time.ctime(os.path.getmtime('rules.cfg')))
        if reload_rules:
            try:
                with open("rules.cfg") as f:
                        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - INFO: New rules found. Loading new rules"
                        clear_rule_list()
                        for line in f:
                            add_rule(line)
            except IOError:
                print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - ERROR: rules.cfg files does not exists or is unreadable"
            finally:
                f.close()
    except IOError:
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - ERROR: rules.cfg files does not exists or is unreadable"


    # rule_update() is called every "rule_read_interval" seconds
    threading.Timer(60, update_rule_list).start()


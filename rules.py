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

def clear_rule_list():
    global rule_list
    rule_list = []

def add_rule(rule):
    rule_list.append(rule)

def get_rule_list():
    return rule_list

def update_rule_list():
    # rule_update() is called every 60 seconds

    # TO-DO check if rules.cfg has been modified or not to reduce file open task
    try:
        with open("rules.cfg") as f:
                print "INFO: New rules found. Loading new rules"
                clear_rule_list()
                for line in f:
                    add_rule(line)
                print rule_list[0]

    except IOError:
        print "ERROR: rules.cfg files does not exists"
        return 0
    finally:
        f.close()

    # rule_update() is called every "rule_read_interval" seconds
    threading.Timer(60, update_rule_list).start()


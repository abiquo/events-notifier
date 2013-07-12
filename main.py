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

from time import sleep
import datetime
import pycurl
from eventing import Event
from rules import update_rule_list
from ruleeditor import ruleEditor
from propertyloader import *

# Receive data event
def on_receive(data):
    # If we received an event
    
    if "timestamp" in data:
        # Instantiate object. (We strip 5 first characters as are not JSON format)
        event = Event(data[5:].strip())
        # Check if event should be notified and do if so
        event.check_event()

if __name__ == '__main__':
    
    # Load required properties from notifier.cfg
    api_ip,api_user,api_pwd,api_port,stream_path = load_api_config()
    retry_interval = load_main_config()
    rule_editor_enabled,rule_editor_port = load_ruleeditor_config()
 
    # Reading rules to detect new ones (This is done every 60 seconds)
    update_rule_list()
   
    if rule_editor_enabled:
        # Start Rule editor Webserver App as thread
        try:
            rule_editor = ruleEditor
            rule_editor.thread_webserver(rule_editor_port)        
        except Exception, e:
            print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - ERROR: An error occurred when loading Rule editor web app"
 
    aborted = False

    while not aborted:    
        try:
            print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - INFO: Connection to %s:%s API Outbound established" % (api_ip,api_port)
            stream_connection = pycurl.Curl()
            stream_connection.setopt(pycurl.USERPWD, "%s:%s" % (api_user, api_pwd))
            stream_connection.setopt(pycurl.URL, "http://%s:%s%s" % (api_ip,api_port,stream_path))
            # Check if pycurl connection is hanged
            # If speed is 1 byte within 7200 seconds connection will be considered as
            # hanged and a reconnection will be thrown
            stream_connection.setopt(pycurl.LOW_SPEED_LIMIT, 1)
            stream_connection.setopt(pycurl.LOW_SPEED_TIME, 7200)
            stream_connection.setopt(pycurl.WRITEFUNCTION, on_receive)
            stream_connection.perform()
 
            if stream_connection.getinfo(pycurl.HTTP_CODE) != 200:
                print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - ERROR: An error occurred connecting to stream, retrying in %s seconds" % (retry_interval)
                sleep(retry_interval)

        except Exception, e:
            print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - ERROR: Connection from server has been terminated or timed out, retrying in %s seconds" % (retry_interval)
            sleep(retry_interval)
    

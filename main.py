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

from rules import *
import sys
from time import sleep
import ConfigParser
import pycurl
import json
from eventing import *

# Receive data event
def on_receive(data):
   # If we received an event
   if "timestamp" in data:
       # Instantiate object
       event = Event(data[5:].strip())
       # Check if event should be notified and do if so
       event.check_event()

if __name__ == '__main__':

    config = ConfigParser.ConfigParser()
    config.read('notifier.cfg')

    api_ip = str(config.get('abiquo', 'api_ip'))
    api_user = str(config.get('abiquo', 'api_user'))
    api_pwd = str(config.get('abiquo', 'api_pwd'))
    api_port = str(config.get('abiquo', 'api_port'))
    stream_path = str(config.get('abiquo', 'stream_path'))

    retry_interval = int(config.get('main', 'retry_interval'))
    aborted = False

    while not aborted:    
        try:
            stream_connection = pycurl.Curl()
            stream_connection.setopt(pycurl.USERPWD, "%s:%s" % (api_user, api_pwd))
            stream_connection.setopt(pycurl.URL, "http://%s:%s%s" % (api_ip,api_port,stream_path))
            stream_connection.setopt(pycurl.WRITEFUNCTION, on_receive)
            stream_connection.perform()
 
            if stream_connection.getinfo(pycurl.HTTP_CODE) != 200:
                print "An error ocurred when connecting to stream"
                sleep(retry_interval)

        except Exception, e:
            print "ERROR: Connection from server has been closed, retrying in %s seconds" % (retry_interval)
            sleep(retry_interval)
#            sys.exit(0)
    

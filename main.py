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
import logging
import sys
import signal
from eventing import Event
from rules import update_rule_list
from ruleeditor import ruleEditor
from propertyloader import *

# Receive data event
def on_receive(data):
    # If we received an event
    if "timestamp" in data:
        # Instantiate object. (We strip 5 first characters as are not JSON format)
        logging.debug("Received event %s" % (data))
        event = Event(data[5:].strip())
        # Check if event should be notified and do if so
        event.check_event()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='./app.log',
                    filemode='w')
    logging.info("App started.")
    # Load required properties from notifier.cfg
    api_url,api_user,api_pwd,api_port,stream_path,ssl_verify_disabled = load_api_config()
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
            logging.error("An error ocurred when loading Rule editor web app")

    aborted = False

    logging.info("Establishing connection to API Outbound at %s:%s%s " % (api_url,api_port,stream_path))
    while not aborted:
        try:
            stream_connection = pycurl.Curl()
            stream_connection.setopt(pycurl.USERPWD, "%s:%s" % (api_user, api_pwd))
            stream_connection.setopt(pycurl.URL, "%s:%s%s" % (api_url,api_port,stream_path))
            # Check if pycurl connection is hanged
            # If speed is 1 byte within 7200 seconds connection will be considered as
            # hanged and a reconnection will be thrown
            stream_connection.setopt(pycurl.LOW_SPEED_LIMIT, 1)
            stream_connection.setopt(pycurl.LOW_SPEED_TIME, 7200)
            stream_connection.setopt(pycurl.WRITEFUNCTION, on_receive)
            if ssl_verify_disabled:
                stream_connection.setopt(pycurl.SSL_VERIFYPEER, 0 )
            stream_connection.perform()

            if stream_connection.getinfo(pycurl.HTTP_CODE) != 200:
                logging.error(" An error occurred [ %s ] connecting to stream, retrying in %s seconds" % (stream_connection.getinfo(pycurl.RESPONSE_CODE), retry_interval))
                sleep(retry_interval)

        except Exception, e:
            logging.error("Connection from server has been terminated or timed out, retrying in %s seconds" % (retry_interval))
            logging.debug("%s" % (e))
            sleep(retry_interval)

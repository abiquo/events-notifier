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

import time
from dateutil import parser
from notifier import send_email
from rules import get_rule_list
import json

### Example data from API Outbound
# {"timestamp":"1370903626167","user":"/admin/enterprises/1/users/1","enterprise":"/admin/enterprises/1","severity":"ERROR","source":"ABIQUO_SERVER","action":"DELETE","type":"DATACENTER","entityIdentifier":"/admin/datacenters/1","details":{"detail":[{"@key":"MESSAGE","$":"Cannot delete datacenter with virtual datacenters associated"},{"@key":"SCOPE","$":"DATACENTER"},{"@key":"CODE","$":"DC-6"}]}}

class Event(object):
    def __init__(self,event_data):
        data = json.loads(event_data)
        self.severity = data['severity']
        self.timestamp = int(data['timestamp'])
        self.performedby = data['user']
        self.enterprise = data['enterprise']
        self.entitytype = data ['type']
        self.entityurl = data['entityIdentifier']
        self.action = data['action']
        self.desc = data['details']

    def check_event(self):
        # When an event is received, we check rule by rule is needs to be notifed
        rule_list = get_rule_list()
        for rule in rule_list:
           # Rule list is in dictionary/json format
           rule_dict = json.loads(rule)
           if ((self.severity == rule_dict['severity'] or rule_dict['severity'] == "all") and 
               (self.action == rule_dict['action'] or rule_dict['action'] == "all") and
               (self.entitytype == rule_dict['entity'] or rule_dict['entity'] == "all") and
               (self.performedby == self.enterprise+"/users/"+rule_dict['user'] or rule_dict['user'] == "all") and
               (self.enterprise == "/admin/enterprise/"+rule_dict['enterprise'] or rule_dict['enterprise'] == "all")):
               # If performedby user rule filter is enabled an enterprise needs to be assigned to the rule too
                   try:
		       # Here is the call to notify by mail the event
                       mail_body = str(self.action)+" description: "+str(self.desc)
                       send_email(str(rule_dict['mailto']),mail_body)
                   except Exception, e:
                       print("An error occurred when sending notifications to %s: %s" %(rule_dict['mailto'],str(e)))


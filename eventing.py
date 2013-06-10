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
import json

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
        print "TO-DO: Check if event needs to be notified"

# Basically, check rule per rule to see if matches with any of them
# WANRNING: Several API calls required, maybe we need to think in put urls in rules instead of users
    

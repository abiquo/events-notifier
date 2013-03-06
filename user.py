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

import pycurl
import StringIO
from xml.dom.minidom import parse, parseString

class User(object):

	def __init__(self,user):
		self.name = self.get_user_value(user, "nick")
		self.email = self.get_user_value(user, "email")

	def get_user_value(self,user,value):
	        if user.getElementsByTagName(value)[0].childNodes:
	                value_return = user.getElementsByTagName(value)[0].childNodes[0].nodeValue
	        else:
	                value_return = ""
	        return value_return

	def get_name(self):
		return str(self.name)
	def get_email(self):
		return str(self.email)
	def __repr__(self):
		out = ''
		out += "Name = %s\n" % self.get_name()
		out += "email = %s\n" % self.get_email()
        	return out + '\n'

	def __str__(self):
	        return self.__repr__()



# Load users of Abiquo
def load_users(ip,user,pwd,port):

	users = []
	url = "http://%s:%s/api/admin/enterprises" %(ip, port)
        user_pwd = '%s:%s' % (user, pwd)
        response = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.WRITEFUNCTION, response.write)
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.USERPWD, user_pwd)
        c.perform()

        try:
		enterprise_list = parseString(response.getvalue()).getElementsByTagName("enterprise")
        except Exception, e:
        	print("An error ocurred when parsing enterprise list: %s" %(str(e)))

        for enterprise in enterprise_list:
		user_list = []

                enterprise_id = enterprise.getElementsByTagName("id")[0].childNodes[0].nodeValue
		url = "http://%s:%s/api/admin/enterprises/%s/users" % (ip, port, enterprise_id)
	        user_pwd = '%s:%s' % (user, pwd)
	        response = StringIO.StringIO()
	        c = pycurl.Curl()
	        c.setopt(pycurl.WRITEFUNCTION, response.write)
		c.setopt(pycurl.URL, str(url))
	        c.setopt(pycurl.USERPWD, user_pwd)
	        c.perform()
		c.close()

                try:
			users_list = parseString(response.getvalue()).getElementsByTagName("user")
                except Exception, e:
                	print("An error ocurred when parsing user list: %s" %(str(e)))
		if users_list:
			for userin in users_list:
				if userin.getElementsByTagName("active")[0].childNodes[0].nodeValue == 'true':
					users.append(User(userin))
	return users
	

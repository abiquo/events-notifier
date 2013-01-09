#!/usr/bin/env python

import pycurl, json
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
def load_users(ip='127.0.0.1',user='root',pwd=''):

	users = []
	url = "http://%s/api/admin/enterprises" % ip
        user_pwd = '%s:%s' % (user, pwd)
        response = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.WRITEFUNCTION, response.write)
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.USERPWD, user_pwd)
        c.perform()

	enterprise_list = parseString(response.getvalue()).getElementsByTagName("enterprise")
        for enterprise in enterprise_list:
                enterprise_id = enterprise.getElementsByTagName("id")[0].childNodes[0].nodeValue
		url = "http://%s/api/admin/enterprises/%s/users" % (ip, enterprise_id)
	        user_pwd = '%s:%s' % (user, pwd)
	        response = StringIO.StringIO()
	        c = pycurl.Curl()
	        c.setopt(pycurl.WRITEFUNCTION, response.write)
		c.setopt(pycurl.URL, str(url))
	        c.setopt(pycurl.USERPWD, user_pwd)
	        c.perform()

		users_list = parseString(response.getvalue()).getElementsByTagName("user")
		for user in users_list:
			users.append(User(user))
        return users


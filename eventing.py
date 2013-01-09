import pycurl, json
import StringIO
import time
from dateutil import parser
from xml.dom.minidom import parse, parseString

class Event(object):
    
    def __init__(self,event=None,timestamp=None):
	if timestamp == None:
		self.id = self.get_event_value(event, "id")
		self.user = self.get_event_value(event,"user")
		self.severity = self.get_event_value(event,"severity")
		self.timestamp = int(time.mktime(parser.parse(self.get_event_value(event,"timestamp")).timetuple()))
		self.performedby = self.get_event_value(event,"performedBy")
		self.action = self.get_event_value(event,"actionPerformed")
		self.desc = self.get_event_value(event,"stacktrace")
	else:
		self.timestamp = timestamp
        
    def get_event_value(self,event,value):
	if event.getElementsByTagName(value)[0].childNodes:
		value_return = event.getElementsByTagName(value)[0].childNodes[0].nodeValue
	else:
		value_return = ""
	return value_return

    def get_id(self):
        return int(self.id)
    def get_user(self):
        return str(self.user)
    def get_severity(self):
        return str(self.severity)
    def get_timestamp(self):
        return str(self.timestamp)
    def get_performedby(self):
        return str(self.performedby)
    def get_action(self):
        return str(self.action)
    def get_desc(self):
        return str(self.desc)
        
    def __repr__(self):
        out = ''
        out += "Timestamp = %s\n" % self.get_timestamp()
        out += "By = %s\n" % self.get_performedby()
        out += "Action = %s\n" % self.get_action()
        out += "Severity = %s\n" % self.get_severity()
        if self.get_desc():
            out += " Info = %s\n" % self.get_desc()

        return out + '\n'
        
    def __str__(self):
        return self.__repr__()

    
def get_new_events(last_event=None,limit = 100,ip='127.0.0.1',user='root',pwd=''):

	if last_event:
		url = "http://%s/api/events?datefrom=%d" % (ip, int(last_event.get_timestamp())+1)
	else:
		url = "http://%s/api/events" % ip
	user_pwd = '%s:%s' % (user, pwd)
	response = StringIO.StringIO()
	c = pycurl.Curl()
	c.setopt(pycurl.WRITEFUNCTION, response.write)
	c.setopt(pycurl.URL, url)
	c.setopt(pycurl.USERPWD, user_pwd)
	c.perform()

	events_list = parseString(response.getvalue()).getElementsByTagName("event")

	events = []
	for event in events_list:
		events.append(Event(event=event))

	return events
    
def events_to_notify(events, actions, owners, sev_levels):
    
    events_filtered = []

    for e in events:
        if (not actions or e.get_action() in actions) and (not owners or e.get_performedby() in owners) and (not sev_levels or e.get_severity() in sev_levels):
                events_filtered.append(e)
            
    return events_filtered

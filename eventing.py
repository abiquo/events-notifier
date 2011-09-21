#!/usr/bin/env python
import MySQLdb

class Event(object):
    
    def __init__(self,id,user,severity,timestamp,performedby,action,desc):
        self.id = id
        self.user = user
        self.severity = severity
        self.timestamp = timestamp
        self.performedby = performedby
        self.action = action
        self.desc = desc
        
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
        return "Id = %d, User = %s, Severity = %s, Timestamp = %s, By = %s, Action = %s, Info = %s" % (self.get_id(), self.get_user(), self.get_severity(), self.get_timestamp(), self.get_performedby(), self.get_action(), self.get_desc())
    def __str__(self):
        return self.__repr__()

    
def get_new_events(last_event=None,limit = 100,dbip='127.0.0.1',dbuser='root',dbpwd=''):
    db = MySQLdb.connect(host=dbip, user=dbuser, passwd=dbpwd, db='kinton')
    cursor = db.cursor()
    sql = ''
    if last_event:
        sql = 'SELECT idMeter,user,severity,timestamp,performedby,actionperformed,stacktrace FROM metering WHERE idMeter > %d ORDER BY idMeter DESC LIMIT %d' % (int(last_event.get_id()), int(limit))
    else:
        sql = 'SELECT idMeter,user,severity,timestamp,performedby,actionperformed,stacktrace FROM metering ORDER BY idMeter DESC LIMIT %d' % (int(limit))

    cursor.execute(sql)
    result = cursor.fetchall()
    
    events = []
    for row in result:
        events.append(Event(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
        
    return events
    
def events_to_notify(events, rule):
    
    events_filtered = []
    for e in events:
        if ( 'all' in rule.get_owners() or e.get_performedby() in rule.get_owners()) and e.get_action() in rule.get_actions():
            events_filtered.append(e)
            
    return events_filtered

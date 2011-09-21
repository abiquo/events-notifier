#!/usr/bin/env python
from rules import *
from notifier import *
from eventing import *
from time import sleep
import pprint

if __name__ == '__main__':

    pp = pprint.PrettyPrinter(indent=4)
    
    # Load DB credentials
    myip,myuser,mypwd = load_db_config()

    last_event = get_new_events(limit=1,dbip=myip,dbuser=myuser,dbpwd=mypwd)[0]
    
    while 1:
        #Get events
        events = get_new_events(last_event,limit=100,dbip=myip,dbuser=myuser,dbpwd=mypwd)
        
        rules = load_rules()
        
        for r in rules:
            #Filter events
            filtered_events = events_to_notify(events, r)
        
            if filtered_events:
                print("New events to notify to user: %s" % (r.get_user()))
                notify_events(r.get_user(), filtered_events, dbip=myip, dbuser=myuser, dbpwd=mypwd)
        if events:
            last_event = events[0]
        
        sleep(5)

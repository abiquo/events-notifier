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
        # Get events
        events = get_new_events(last_event,limit=100,dbip=myip,dbuser=myuser,dbpwd=mypwd)
        
        rules = load_rules()
        
        for r in rules:
            # Load users
            users = []
            if r.get_user() == 'all':
                users = load_users(dbip=myip,dbuser=myuser,dbpwd=mypwd)
            else:
                users.append(r.get_user())

            # Load actions
            actions = r.get_actions()
            if 'all' in actions:
                # Do not filter by Action
                action = []
            
            # Load owners
            owners = r.get_owners()
            if 'all' in owners:
                owners = load_users(dbip=myip,dbuser=myuser,dbpwd=mypwd)
            elif not owners:
                owners = [r.get_user()]
                
            # Load severity levels
            sev_levels = r.get_levels()
            if 'all' in sev_levels:
                # Do not filter by Severity
                sev_levels = []
            
            # Filter events
            for u in users:
                filtered_events = events_to_notify(events, actions, owners, sev_levels)
        
                if filtered_events:
                    print("New events to notify to user: %s" % (u))
                    notify_events(u, filtered_events, dbip=myip, dbuser=myuser, dbpwd=mypwd)
        if events:
            last_event = events[0]
        
        sleep(5)

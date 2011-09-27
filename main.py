#!/usr/bin/env python
from rules import *
from notifier import *
from eventing import *
from time import sleep

if __name__ == '__main__':

    # Load DB credentials
    myip,myuser,mypwd = load_db_config()

    last_event = None

    try:
        last_event = get_new_events(limit=1,dbip=myip,dbuser=myuser,dbpwd=mypwd)[0]
    except Exception, e:
        print("An error ocurred when accessing the database: %s" %(str(e)))
        
    while 1:
    
        events = []
    
        # Get events
        try:
            events = get_new_events(last_event,limit=100,dbip=myip,dbuser=myuser,dbpwd=mypwd)
        except Exception, e:
            print("An error ocurred when retrieving events from %s: %s" %(myip, str(e)))

        # Look all users that have any rule
        for user in load_users_from_rules():

            filtered_events = []
            
            rules = []
            try:
                # Load user's rules
                rules = load_rules_from_user(user)
                rules.extend(load_rules_from_user('all'))
            except Exception, e:
                print("An error ocurred when loading rules: %s" %(str(e)))

            
            for r in rules:
                # Load actions
                actions = r.get_actions()
                if 'all' in actions:
                    # Do not filter by Action
                    action = []
                
                # Load owners
                owners = r.get_owners()
                if 'all' in owners:
                    owners = []
                #If owners is not set, only filter events whose owner is the user.
                elif not owners:
                    owners = [r.get_user()]
                    
                # Load severity levels
                sev_levels = r.get_levels()
                if 'all' in sev_levels:
                    # Do not filter by Severity
                    sev_levels = []
                
                # Filter events and add to the list
                filtered_events.extend(events_to_notify(events, actions, owners, sev_levels))
            
            if filtered_events:
                print("New events to notify to user: %s" % (user))
                try:
                    notify_events(user, filtered_events, dbip=myip, dbuser=myuser, dbpwd=mypwd)
                except Exception, e:
                    print("An error ocurred when sending notifications to %s: %s" %(user,str(e)))

        if events:
            last_event = events[0]
        
        sleep(5)

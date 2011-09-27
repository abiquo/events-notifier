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
            
        if not events:
            sleep(5)
            continue

        # Look for all users
        for user in load_users(dbip=myip,dbuser=myuser,dbpwd=mypwd):

            filtered_events = []
            
            rules = []
            try:
                # Load user's rules
                rules = load_rules_from_user(user)
                # Include user 'all' rules
                rules.extend(load_rules_from_user('all'))
            except Exception, e:
                print("An error ocurred when loading rules: %s" %(str(e)))

            
            for r in rules:
                # Load filters
                actions = r.get_actions()
                owners = r.get_owners()
                if r.get_user() == 'all':
                    owners = [user]
                sev_levels = r.get_levels()
                
                # Filter events and add to the list
                filtered_events.extend(events_to_notify(events, actions, owners, sev_levels))
            
            if filtered_events:
                print("New events to notify to user: %s" % (user))
                print("Events to notify: %s"%(filtered_events))

                try:
                    notify_events(user, filtered_events, dbip=myip, dbuser=myuser, dbpwd=mypwd)
                except Exception, e:
                    print("An error ocurred when sending notifications to %s: %s" %(user,str(e)))

        if events:
            last_event = events[0]
        
        sleep(5)

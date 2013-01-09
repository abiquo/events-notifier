#!/usr/bin/env python
from rules import *
from notifier import *
from eventing import *
from user import *
from time import sleep
import ConfigParser

if __name__ == '__main__':

    # Load DB credentials
    myip,myuser,mypwd = load_db_config()

    last_event = None

    config = ConfigParser.ConfigParser()
    config.read('notifier.cfg')

    interval = int(config.get('main', 'polling_interval'))

    try:
	last_event = Event(timestamp=int(time.time()))
    except Exception, e:
        print("An error ocurred when accessing the database: %s" %(str(e)))
        
    while 1:
    
        events = []
    
        # Get events
        try:
            events = get_new_events(last_event,limit=100,ip=myip,user=myuser,pwd=mypwd)
        except Exception, e:
            print("An error ocurred when retrieving events from %s: %s" %(myip, str(e)))
            
        if not events:
            sleep(interval)
            continue

        # Look for all users
        for user in load_users(ip=myip,user=myuser,pwd=mypwd):

            filtered_events = []
            
            rules = []
            try:
                # Load user's rules
                rules = load_rules_from_user(user.get_name())
                # Include user 'all' rules
                rules.extend(load_rules_from_user('all'))
            except Exception, e:
                print("An error ocurred when loading rules: %s" %(str(e)))

            
            for r in rules:
                # Load filters
                actions = r.get_actions()
                owners = r.get_owners()
                if r.get_user() == 'all':
                    owners = [user.get_name()]
                sev_levels = r.get_levels()
                
                # Filter events and add to the list
                filtered_events.extend(events_to_notify(events, actions, owners, sev_levels))
            
            if filtered_events:
                print("New events to notify to user: %s" % (user.get_name()))
                print("Events to notify: %s"%(filtered_events))

                try:
                    notify_events(user, filtered_events)
                except Exception, e:
                    print("An error ocurred when sending notifications to %s: %s" %(user,str(e)))

        if events:
            last_event = events[0]
        
        sleep(interval)

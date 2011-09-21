#!/usr/bin/env python
from rules import *
import sys, getopt

def usage():
    print "Usage: add_rule.py --user USER --actions ACTION1,...,ACTIONN --owners OWNER1,...,OWNERN "
    print "Add a new rule to the Abiquo Events Notifier.\n"
    print "-u\t--user=USER\tTarget user of the rule"
    print "-a\t--actions=ACTIONS\tComma separated list of actions to monitor"
    print "-o\t--owners=OWNERS\t\tComma separated list of owners to filter by. Use 'all' for monitor any owner"
    print "-l\t--list-actions\t\tList all allowed actions"
    print ""

def list_actions():
    print "VAPP_CREATE - When a VAPP is created"
    print "VAPP_DELETE - When a VAPP is deleted"
    #TODO

def main():
    
    user=''
    actions=[]
    owners=[]

    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:a:o:l", ["user=", "actions=", "owners=", "list-actions"])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)

    for o, a in opts:
        if o in ("-l", "--list-actions"):
            list_actions()
            sys.exit()
        elif o in ("-u", "--user"):
            user = a.strip()
        elif o in ("-a", "--actions"):
            for action in a.split(','):
                actions.append(action.strip())
        elif o in ("-o", "--owners"):
            for owner in a.split(','):
                owners.append(owner.strip())
    
    if not (user and actions and owners):
        usage()
        return

    """
    print "Add the rule which will filter events"
    print "If a rule already exists for the target user, it will be replaced"

    user = raw_input("Target user (must be present in Abiquo): ")
    actions = raw_input("Actions: ")
    owners = raw_input("Owners: ")
    """
    
    rule = Rule(user.strip())

    for a in actions:
        rule.add_action(a)
    
    for o in owners:
        rule.add_owner(o)
    
    save_rule(rule)
    
    print("Rule added!")

if __name__ == '__main__':
    main()

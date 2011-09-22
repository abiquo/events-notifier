#!/usr/bin/env python
from rules import *
import sys, getopt

def usage():
    print "Usage: add_rule.py --user USER [--actions ACTION1,...,ACTIONN] [ --owners OWNER1,...,OWNERN ] [ --severity LEVEL1,...,LEVELN ]"
    print "Add a new rule to the Abiquo Events Notifier.\n"
    print "-u\t--user=USER\tTarget user to be notified. Use all to this rule affect all users"
    print "-a\t--actions=ACTIONS\tComma separated list of actions to monitor"
    print "-o\t--owners=OWNERS\t\tComma separated list of owners to filter by. Use 'all' for monitor any owner. If no owner is specified, only monitors actions performed by user"
    print "-s\t--severity=LEVELS\t\tComma separated list of levels of severity to filter by. Use 'all' for monitor any level."
    print "--list-actions\t\tList all allowed actions"
    print "--list-severity-levels\t\tList all severity levels"
    print ""

def list_actions():
    print "VAPP_CREATE - When a VAPP is created"
    print "VAPP_DELETE - When a VAPP is deleted"
    #TODO
    
def list_severity_levels():
    print("INFO\nWARNING\nMINOR\nNORMAL\nMAJOR\nCRITICAL")

def main():
    
    user=''
    actions=[]
    owners=[]
    sev_levels=[]

    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:a:o:s:LS", ["user=", "actions=", "owners=", "severity=", "list-actions", "list-severity-levels"])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)

    for o, a in opts:
        if o in ("-L", "--list-actions"):
            list_actions()
            sys.exit()
        elif o in ("-S", "--list-severity-levels"):
            list_severity_levels()
            sys.exit()
        elif o in ("-u", "--user"):
            user = a.strip()
        elif o in ("-a", "--actions"):
            for action in a.split(','):
                actions.append(action.strip())
        elif o in ("-o", "--owners"):
            for owner in a.split(','):
                owners.append(owner.strip())
        elif o in ("-s", "--severity"):
            for level in a.split(','):
                sev_levels.append(level.strip())
    
    if not (user):
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

    if actions:
        for a in actions:
            rule.add_action(a)
    
    if owners:
        for o in owners:
            rule.add_owner(o)
            
    if sev_levels:
        for s in sev_levels:
            rule.add_level(s)
            
    save_rule(rule)
    
    print("Rule added!")

if __name__ == '__main__':
    main()

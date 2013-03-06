#!/usr/bin/env python

#	The Abiquo Platform
#	Cloud management application for hybrid clouds
#	Copyright (C) 2008-2013 - Abiquo Holding S.L. 
#
#	This application is free software; you can redistribute it and/or
#	modify it under the terms of the GNU LESSER GENERAL PUBLIC
#	LICENSE as published by the Free Software Foundation under
#	version 3 of the License
#
#	This software is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#	LESSER GENERAL PUBLIC LICENSE v.3 for more details.
#
#	You should have received a copy of the GNU Lesser General Public
#	License along with this library; if not, write to the
#	Free Software Foundation, Inc., 59 Temple Place - Suite 330,
#	Boston, MA 02111-1307, USA.

from rules import *
import sys, getopt

def usage():
    print "Usage: add_rule.py --user USER [--actions ACTION1,...,ACTIONN] [ --owners OWNER1,...,OWNERN ] [ --severity LEVEL1,...,LEVELN ]"
    print "Add a new rule to the Abiquo Events Notifier.\n"
    print "-u\t--user=USER\tTarget user to be notified. Use all to this rule affect all users"
    print "-a\t--actions=ACTIONS\tComma separated list of actions to monitor"
    print "-o\t--owners=OWNERS\t\tComma separated list of owners to filter by. Use 'all' for monitor any owner. If no owner is specified, only monitors actions performed by user"
    print "-s\t--severity=LEVELS\t\tComma separated list of levels of severity to filter by. Use 'all' for monitor any level."
    print ""

def main():
    
    user=''
    actions=[]
    owners=[]
    sev_levels=[]

    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:a:o:s:", ["user=", "actions=", "owners=", "severity="])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)

    for o, a in opts:
        if o in ("-u", "--user"):
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

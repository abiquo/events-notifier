#!/usr/bin/env python

#       The Abiquo Platform
#       Cloud management application for hybrid clouds
#       Copyright (C) 2008-2013 - Abiquo Holding S.L. 
#
#       This application is free software; you can redistribute it and/or
#       modify it under the terms of the GNU LESSER GENERAL PUBLIC
#       LICENSE as published by the Free Software Foundation under
#       version 3 of the License
#
#       This software is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#       LESSER GENERAL PUBLIC LICENSE v.3 for more details.
#
#       You should have received a copy of the GNU Lesser General Public
#       License along with this library; if not, write to the
#       Free Software Foundation, Inc., 59 Temple Place - Suite 330,
#       Boston, MA 02111-1307, USA.

from rules import load_rules, delete_rule
import sys

if __name__ == "__main__":
    rules = []
    rules = load_rules()

    i = 0 
    for rule in rules:
        print "%d - %s" %(rule[0], rule[1])
        i += 1

    if i == 0:
        print "No rules found"
    else:
        try:
            print "Which rule do you want to delete?" 
            rule_n = int(raw_input())
        except ValueError:
            print 'Invalid Number'
        
        if delete_rule(rule_n):
            print "Rule deleted"
        else:
            print  "Rule not found"

        

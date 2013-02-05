#!/usr/bin/env python
from rules import load_rules, delete_rule
import sys

if __name__ == "__main__":
    rules = []
    rules = load_rules()

    i = 0 
    for rule in rules:
        print "%d - %s" %(i, rule)
        i += 1

    if i == 0:
        print "No rules found"
    else:
        try:
            print "Which rule do you want to delete?" 
            rule_n = int(raw_input())
        except ValueError:
            print 'Invalid Number'
        
        if delete_rule(rule_n+1):
            print "Rule deleted"
        else:
            print  "Rule not found"

        

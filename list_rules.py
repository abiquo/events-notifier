#!/usr/bin/env python
from rules import load_rules_from_user,load_users_from_rules

if __name__ == "__main__":

    for u in load_users_from_rules():
        print("\nUser: " + u)        

        for r in load_rules_from_user(u):
            print("\t"+"-"*46)
            print("\tActions: " + str(r.get_actions()))
            print("\tOwners: " + str(r.get_owners()))
            print("\tSeverity Levels: " + str(r.get_levels()))
            print("\t"+"-"*46)


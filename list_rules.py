#!/usr/bin/env python
from rules import load_rules

if __name__ == "__main__":

    for r in load_rules():
        print("-"*50)
        print("User: " + r.get_user())
        print("Actions: " + str(r.get_actions()))
        print("Owners: " + str(r.get_owners()))
        print("-"*50)

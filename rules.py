#!/usr/bin/env python

import pickle
import sqlite
from os import system
import base64

class Rule(object):
    
    def __init__(self,user):
        self.user = user
        self.actions = []
        self.owners = []
        self.levels = []

    def get_user(self):
        return str(self.user)
 
    def get_actions(self):
        return self.actions

    def get_owners(self):
        return self.owners

    def get_levels(self):
        return self.levels
    
    def add_action(self,action):
        if str(action) not in self.actions:
            self.actions.append(str(action))

    def add_owner(self,user):
        if str(user) not in self.owners:
            self.owners.append(str(user))
    
    def add_level(self,level):
        if str(level) not in self.levels:
            self.levels.append(str(level))
        
    def del_action(self,action):
        if str(action) in self.actions:
            self.actions.remove(str(action))
            
    def del_owner(self,user):
        if str(user) in self.owners:
            self.owners.remove(str(user))
    
    def del_level(self,level):
        if str(level) in self.levels:
            self.levels.remove(str(level))
            
    def __repr__(self):
        return "User = %s, Actions = %s, Action's owners = %s, Severity Levels = %s" % (self.get_user(), self.get_actions(), self.get_owners(), self.get_levels())

    def __str__(self):
        return self.__repr__()
          
def save_rule(rule):
    con = sqlite.connect('rules.db')
    c = con.cursor()
    
    c.execute("SELECT rule FROM rules WHERE user = '%s' " %(rule.get_user()) )
    row = c.fetchone()
    
    if row:
        rule64 = base64.b64encode(pickle.dumps(rule))
        sql = "UPDATE rules SET rule = '%s' WHERE user = '%s' " %(rule64, rule.get_user())
    else:
        rule64 = base64.b64encode(pickle.dumps(rule))
        sql = "INSERT INTO rules (user, rule) VALUES ('%s', '%s')" %(rule.get_user(),rule64)

    c.execute(sql)
    con.commit()
    c.close()
    con.close()
            
def load_rule(user):
    con = sqlite.connect('rules.db')
    c = con.cursor()

    c.execute("SELECT rule FROM rules WHERE user = '%s' " %(user) )
    rule64 = c.fetchone()
    
    if rule64:
        return pickle.loads(base64.b64decode(rule64[0]))
        
    c.close()
    con.close()
    
def load_rules():
    con = sqlite.connect('rules.db')
    c = con.cursor()

    c.execute("SELECT rule FROM rules" )
    result = c.fetchall()
    
    rules = []
    for rule64 in result:
        rules.append(pickle.loads(base64.b64decode(rule64[0])))
        
    c.close()
    con.close()
    
    return rules

def init_rules():
    try:
        system('rm -f rules.db')
        con = sqlite.connect('rules.db')
        c = con.cursor()
        c.execute('CREATE TABLE rules (user VARCHAR(128), rule TEXT)')
        con.commit()
        c.close()
        con.close()
    except Exception:
        raise

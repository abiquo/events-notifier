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

    def __eq__(self, other):
        if isinstance(other, Rule):
            return (self.user == other.user) and (self.owners.sort() == other.owners.sort()) and (self.actions.sort() == other.actions.sort()) and (self.levels.sort() == other.levels.sort())
        return NotImplemented
          
def save_rule(rule):
    con = sqlite.connect('rules.db')
    c = con.cursor()
    
    rule64 = base64.b64encode(pickle.dumps(rule))
    sql = "INSERT INTO rules (user, rule) VALUES ('%s', '%s')" %(rule.get_user(),rule64)
    c.execute(sql)

    con.commit()
    c.close()
    con.close()

def load_users_from_rules():
    con = sqlite.connect('rules.db')
    c = con.cursor()

    c.execute("SELECT distinct(user) FROM rules")
    result = c.fetchall()
    
    users = []
    for r in result:
        users.append(r[0])
        
    c.close()
    con.close()
    
    return users
            
def load_rules_from_user(user):
    con = sqlite.connect('rules.db')
    c = con.cursor()

    c.execute("SELECT rule FROM rules WHERE user = '%s' " %(user) )
    rules64 = c.fetchall()
    
    rules = []
    for r in rules64:
        rule = pickle.loads(base64.b64decode(r[0]))
        rules.append(rule)
        
    c.close()
    con.close()
    
    return rules

def load_rules():
    con = sqlite.connect('rules.db')
    c = con.cursor()

    c.execute("select rowid, rule from rules" )
    result = c.fetchall()
    print result
    
    rules = []
    for rule64 in result:
        rules.append((rule64[0], pickle.loads(base64.b64decode(rule64[1]))))
        
    c.close()
    con.close()
    
    return rules

def delete_rule(rule):
    found = 0
    con = sqlite.connect('rules.db')
    c = con.cursor()

    c.execute("delete from rules where rowid == '%s'" %(rule))
    found = 2
     
    con.commit()
    c.close()
    con.close()

    return found

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


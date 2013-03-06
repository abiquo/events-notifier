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


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

from user import *

# Send an email to a user with the specified content (list of events)
def send_email(to, content):
    import smtplib
    
    FROM, SUBJECT, BODY, IP, PORT = load_email_config()
    
    body = "From: %s\nSubject: %s\n\n%s\n\n" % (FROM, SUBJECT, BODY)
    for e in content:
        body += str(e) + "\n"
    
    try:
       smtpObj = smtplib.SMTP(IP, PORT)
       smtpObj.sendmail(FROM, [to], body)         
    except smtplib.SMTPException:
        raise

# Notify via email the list of events.
def notify_events(user, events):
    
    email = user.get_email();
    if email:
        send_email(email, events)
    
def load_db_config():
    import ConfigParser

    config = ConfigParser.ConfigParser()
    config.read('notifier.cfg')

    api_ip = config.get('abiquo', 'api_ip')
    api_user = config.get('abiquo', 'api_user')
    api_pwd = config.get('abiquo', 'api_pwd')
    api_port = config.get('abiquo', 'api_port')
    
    return (api_ip, api_user, api_pwd, api_port)

def load_email_config():
    import ConfigParser

    config = ConfigParser.ConfigParser()
    config.read('notifier.cfg')

    f = config.get('email', 'from')
    s = config.get('email', 'subject')
    b = config.get('email', 'body')
    ip = config.get('email', 'smtp_ip')
    port = config.get('email', 'smtp_port')
    
    return (f, s, b, ip, port)
    


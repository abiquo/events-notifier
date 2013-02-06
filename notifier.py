#!/usr/bin/env python
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
    


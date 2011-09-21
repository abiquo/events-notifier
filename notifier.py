#!/usr/bin/env python
import MySQLdb

def get_email_from_user(user, dbip='127.0.0.1',dbuser='root',dbpwd=''):
    db = MySQLdb.connect(host=dbip, user=dbuser, passwd=dbpwd, db='kinton')
    cursor = db.cursor()

    sql = "SELECT email FROM user WHERE user = '%s'" % (str(user))
    cursor.execute(sql)
    
    result = cursor.fetchone()
    
    if result:
        cursor.close()
        db.close()
        return result[0]
    
    return None

# Send an email to a user with the specified content (list of events)
def send_email(to, content):
    import smtplib
    
    FROM, SUBJECT, BODY, IP, PORT = load_email_config()
    
    body = "Subject: %s\n\n%s\n\n" % (SUBJECT, BODY)
    for e in content:
        body += str(e) + "\n"
    
    try:
       smtpObj = smtplib.SMTP(IP, PORT)
       smtpObj.sendmail(FROM, [to], body)         
    except smtplib.SMTPException:
        raise


# Notify via email the list of events.
def notify_events(user, events, dbip='127.0.0.1', dbuser='root', dbpwd=''):
    email = get_email_from_user(user, dbip, dbuser,dbpwd)
    if email:
        send_email(email, events)
    
def load_db_config():
    import ConfigParser

    config = ConfigParser.ConfigParser()
    config.read('notifier.cfg')

    ip = config.get('mysql', 'ip')
    user = config.get('mysql', 'user')
    pwd = config.get('mysql', 'pwd')
    
    return (ip, user, pwd)

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
    


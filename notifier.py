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

import datetime
import ConfigParser
import smtplib
import pycurl
import StringIO
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from xml.dom.minidom import parse, parseString

def send_email(to, event_to_notify):

    # Exit if no email address to send
    if not to:
        return
    
    content = event_to_html(event_to_notify)
    
    FROM, SUBJECT, IP, PORT = load_email_config()

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT+ " " + str(event_to_notify.get_timestamp())
    msg['From'] = FROM
    msg['To'] = to

    text = "This client cannot load HTML content"

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(content, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    try:
        s = smtplib.SMTP(IP, PORT)
        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        s.sendmail(FROM,to, msg.as_string())
        s.quit()
    except smtplib.SMTPException:
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - ERROR: An error occurred when sending mail to SMTP Server"
        raise

def load_email_config():
    config = ConfigParser.ConfigParser()
    config.read('notifier.cfg')

    f = config.get('email', 'from')
    s = config.get('email', 'subject')
    ip = config.get('email', 'smtp_ip')
    port = config.get('email', 'smtp_port')
    
    return (f, s, ip, port)

def load_api_config():
    config = ConfigParser.ConfigParser()
    config.read('notifier.cfg')
    api_ip = config.get('abiquo', 'api_ip')
    api_user = config.get('abiquo', 'api_user')
    api_pwd = config.get('abiquo', 'api_pwd')
    api_port = config.get('abiquo', 'api_port')
    return (api_ip, api_user, api_pwd, api_port)

def event_to_html(event):
    
    #########################
    ### Get event details ###
    #########################
    
    # Timestamp returned by API Outbound is in Java millisecond format, we need to divide by 1000
    timestamp_to_datestring = datetime.datetime.fromtimestamp(event.get_timestamp()/1000).strftime('%Y-%m-%d %H:%M:%S')
    
    api_ip,api_user,api_pwd,api_port = load_api_config()
    
    # Check if event has been performed by SYSTEM or an user
    if event.get_performedby()=='SYSTEM':
        user_name = 'SYSTEM'
        user_surname = ""
        user_nick = ""
        user_email = ""
    # If event has been performed by an user, get its details by doing an API call
    elif event.get_performedby() and event.get_performedby()!='SYSTEM':     
        try:
            user_details = []
            url = "http://%s:%s/api/%s" % (api_ip, api_port, event.get_performedby())
            user_pwd = '%s:%s' % (api_user, api_pwd)
            response = StringIO.StringIO()
            c = pycurl.Curl()
            c.setopt(pycurl.WRITEFUNCTION, response.write)
            c.setopt(pycurl.URL, str(url))
            c.setopt(pycurl.USERPWD, user_pwd)
            c.perform()
            
            user_details = parseString(response.getvalue()).getElementsByTagName("user")
            
            for user in user_details:
                user_name = user.getElementsByTagName("name")[0].childNodes[0].nodeValue
                user_surname = user.getElementsByTagName("surname")[0].childNodes[0].nodeValue
                user_nick = user.getElementsByTagName("nick")[0].childNodes[0].nodeValue
                user_email = user.getElementsByTagName("email")[0].childNodes[0].nodeValue
        except Exception, e:
            print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - ERROR: An error occurred retrieving user-performedby data: "+e
        finally:
            c.close()
    # Make "beauty" severity text depending if is INFO,WARN or ERROR 
    if event.get_severity()=='INFO':
        severity_row="""<td style="padding: 4px 5px;line-height: 20px;text-align: left;vertical-align: top;border-top: 1px solid #ddd"><span class="label label-warning" style="display: inline-block;padding: 2px 4px;font-size: 11.844px;font-weight: bold;line-height: 14px;color: #fff;text-shadow: 0 -1px 0 rgba(0, 0, 0, 0.25);white-space: nowrap;vertical-align: baseline;background-color: #0000CD;-webkit-border-radius: 3px;-moz-border-radius: 3px;border-radius: 3px">INFO</span></td>"""    
    elif event.get_severity()=='WARN':
        severity_row="""<td style="padding: 4px 5px;line-height: 20px;text-align: left;vertical-align: top;border-top: 1px solid #ddd"><span class="label label-warning" style="display: inline-block;padding: 2px 4px;font-size: 11.844px;font-weight: bold;line-height: 14px;color: #fff;text-shadow: 0 -1px 0 rgba(0, 0, 0, 0.25);white-space: nowrap;vertical-align: baseline;background-color: #FFA500;-webkit-border-radius: 3px;-moz-border-radius: 3px;border-radius: 3px">WARNING</span></td>"""        
    else:
        severity_row="""<td style="padding: 4px 5px;line-height: 20px;text-align: left;vertical-align: top;border-top: 1px solid #ddd"><span class="label label-warning" style="display: inline-block;padding: 2px 4px;font-size: 11.844px;font-weight: bold;line-height: 14px;color: #fff;text-shadow: 0 -1px 0 rgba(0, 0, 0, 0.25);white-space: nowrap;vertical-align: baseline;background-color: #FF0000;-webkit-border-radius: 3px;-moz-border-radius: 3px;border-radius: 3px">ERROR</span></td>"""
    
    #############################
    ### Generate HTML message ###
    #############################
    content = ""
    
    content += """
        <html>
            <head>
                <title>Abiquo action notification</title>
            </head>
            <body bgcolor="#E6E6FA" style="margin: 0;font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif;font-size: 14px;line-height: 20px;color: #333;background-color: #fff">
                <p style="margin: 0 0 10px"/><div style="padding: 19px 19px;width: 940px;margin-right: auto;margin-left: auto;min-height: 20px;margin-bottom: 20px;background-color: #f5f5f5;border: 1px solid #e3e3e3;-webkit-border-radius: 6px;-moz-border-radius: 6px;border-radius: 6px;-webkit-box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.05);-moz-box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.05);box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.05)">
                <p style="margin: 0 0 10px;text-align: center"/><h1 style="margin: 10px 0;font-family: inherit;font-weight: bold;line-height: 20px;color: inherit;text-rendering: optimizelegibility;font-size: 38.5px">Abiquo action notification</h1>
                <br><span>The action was:<br><br></span>
        
                <div>
                    <table style="max-width: 100%;background-color: transparent;border-collapse: collapse;border-spacing: 0;width: 100%;margin-bottom: 20px">
                        <tbody>
                            <tr>
                                <td style="padding: 4px 5px;line-height: 20px;text-align: left;vertical-align: top;border-top: 1px solid #ddd"><strong style="font-weight: bold">Performed at: </strong> </td>
                                <td style="padding: 4px 5px;line-height: 20px;text-align: left;vertical-align: top;border-top: 1px solid #ddd">"""+timestamp_to_datestring+"""</td>
                            </tr>
                           <tr>
                                <td style="padding: 4px 5px;line-height: 20px;text-align: left;vertical-align: top;border-top: 1px solid #ddd"><strong style="font-weight: bold">Performed by: </strong> </td>
                                <td style="padding: 4px 5px;line-height: 20px;text-align: left;vertical-align: top;border-top: 1px solid #ddd">"""+user_name.capitalize()+" "+user_surname.capitalize()+" - "+user_nick+" - "+user_email+"""</td>
                            </tr>
                            <tr>
                                <td style="padding: 4px 5px;line-height: 20px;text-align: left;vertical-align: top;border-top: 1px solid #ddd"><strong style="font-weight: bold">Action: </strong> </td>
                                <td style="padding: 4px 5px;line-height: 20px;text-align: left;vertical-align: top;border-top: 1px solid #ddd">"""+str(event.get_action())+"""</td>
                            </tr>
                            <tr>
                                <td style="padding: 4px 5px;line-height: 20px;text-align: left;vertical-align: top;border-top: 1px solid #ddd"><strong style="font-weight: bold">Entity: </strong> </td>
                                <td style="padding: 4px 5px;line-height: 20px;text-align: left;vertical-align: top;border-top: 1px solid #ddd">"""+str(event.get_entitytype())+"""</td>
                            </tr>
                            <tr>
                                <td style="padding: 4px 5px;line-height: 20px;text-align: left;vertical-align: top;border-top: 1px solid #ddd"><strong style="font-weight: bold">Severity: </strong> </td>"""+severity_row+"""</tr>
                            <tr>
                                <td style="padding: 4px 5px;line-height: 20px;text-align: left;vertical-align: top;border-top: 1px solid #ddd"><strong style="font-weight: bold">Details: </strong> </td>
                                <td style="padding: 4px 5px;line-height: 20px;text-align: left;vertical-align: top;border-top: 1px solid #ddd"></td>
                            </tr><tr><td></td><td></td></tr>"""
    # Add stacktrace/description details to HTML message
    for key,value in dict.iteritems(event.get_description()):
        content += "<tr>"
        content += """<td style="padding: 4px 5px;line-height: 20px;text-align: left;vertical-align: top">"""+key+"""</td>"""
        content += """<td style="padding: 4px 5px;line-height: 20px;text-align: left;vertical-align: top">"""+value+"""</td>"""
        content += "</tr>"
    
    content += """</tbody></table></div></body></html>"""
    
    return content

    

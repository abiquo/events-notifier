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

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
from threading import Thread
import datetime
import json
import urlparse
import os

class ruleEditor(BaseHTTPRequestHandler):
    def do_GET(self):
        
        # URL Parameters
        params = urlparse.parse_qs(self.path)

        # Check if URL has action and data parameters
        if params.has_key("action"):
            if params["action"][0] == "delete":
                try:
		    f = open("rules.cfg","r")
		    working = open("rules_tmp.cfg", "w")
                    line_number=0 
                    for line in f:    
                        if line_number != int(params["data"][0]):
                            working.write(line)
                        line_number+=1
                except IOError:
                    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - ERROR: rules.cfg files does not exist or is unreadable"
                    return 0
                finally:
                    f.close()
		    working.close()
                
                try:
                    os.rename("rules_tmp.cfg", "rules.cfg")
                    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - INFO: Notifier rule has been deleted"
                    # Redirect to / to avoid parameters in the URL
                    self.path = ""
                    self.send_response(301)
                    self.send_header('Location','/')
                    self.end_headers()
                    return

                except Exception,e :
                    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - ERROR: An error occurred when modifying rules.cfg" 
        # If parameter rule_mail exists in the URL, this means that rule add action has been executed
        elif params.has_key("rule_email"):
                try:
                    # Compose new_rule from passed parameters
                    new_rule = '{ "mailto" : "'+params["rule_email"][0]+'" , "action" : "'+params["rule_action"][0]+'" , "entity" : "'+params["rule_entity"][0]+'" , "severity" : "'+params["rule_severity"][0]+'" , "user" : "'+params["rule_user"][0]+'" , "enterprise" : "'+params["rule_enterprise"][0]+'" }\n'
                    with open("rules.cfg","a") as f:
                        f.write(new_rule)
                    # Redirect to / to avoid parameters in the URL
                    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - INFO: Notifier rule has been added:"
                    print new_rule
                    self.path = ""
                    self.send_response(301)
                    self.send_header('Location','/')
                    self.end_headers()
                except IOError:
                    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - ERROR: rules.cfg files does not exist or is unreadable"
                    return 0
                finally:
                    f.close()

            
        self.send_response(200)
        self.send_header('Content-type','text/html')        
        self.end_headers()
        # Rule editor Form
        self.wfile.write(''' 
            <html> 
            <head> 
            <title> Abiquo events-notifier Rule editor </title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <!-- Bootstrap -->
            <link href="http://twitter.github.io/bootstrap/assets/css/bootstrap.css" rel="stylesheet" media="screen"> 
            </head> 
            <body> 
            <p class="text-center"><h1>Abiquo events-notifier rules</h1></p>
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>Mail to</th>
                  <th>Action</th>
                  <th>Entity</th>
                  <th>Severity</th>
                  <th>idUser</th>
                  <th>idEnterprise</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>''')
        
        try:
            with open("rules.cfg") as f:
                line_number=0
                for line in f:
		    try:
                        rule_dict = json.loads(line)
		    except ValueError:
			print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - ERROR: rules.cfg files is not well formated. Review it to fit format"
                        return 0
                    self.wfile.write('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><a href="./?modify&action=delete&data=%s"><button type="button" class="btn btn-danger">Delete</button></a></td></tr>' % (str(rule_dict['mailto']),str(rule_dict['action']),str(rule_dict['entity']),str(rule_dict['severity']),str(rule_dict['user']),str(rule_dict['enterprise']),line_number))
                    line_number+=1
                    
        except IOError:
            print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - ERROR: rules.cfg files does not exist or is unreadable"
            return 0
        finally:
                f.close()

        self.wfile.write('''
            <form action="" method="get">
            <tr>
            <input type="hidden" name="action" value="add">
            <td><input type="email" required name="rule_email"></td>
            <td><input type="text" required name="rule_action"></td>
            <td><input type="text" required name="rule_entity"></td>
            <td><input type="text" required name="rule_severity"></td>
            <td><input type="text" class="span1" required name="rule_user"></td>
            <td><input type="text" class="span1" required name="rule_enterprise"></td>
            <td><input type="submit" class="btn btn-info" value="Add"></td>
            </form>
            </tr>
            </tbody>
            </table>
            </div>
            </body> 
            </html> 
        ''')
        return
        
    # Silent webserver, no output on connection.
    # This can be commented for debug
    #def log_message(self, format, *args):
    #    return

    @staticmethod
    def start_webserver(rule_editor_port):
        try:
            server = ThreadingHTTPServer(('', rule_editor_port), ruleEditor)
            print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' - INFO: Rule editor Webapp started listening at port %s' % (rule_editor_port)
            server.serve_forever()
        except Exception, e:
                print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - ERROR: An error occurred when starting Rule editor web server"
                print e

    @staticmethod
    def thread_webserver(rule_editor_port):
        Thread(target=ruleEditor.start_webserver, args=[rule_editor_port]).start()
    
class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass


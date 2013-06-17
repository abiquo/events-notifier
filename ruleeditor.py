import cgi
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
from threading import Thread
import datetime
import json

class ruleEditor(BaseHTTPRequestHandler):

    def do_GET(self):
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
                    rule_dict = json.loads(line)
                    self.wfile.write('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><button type="button" class="btn btn-danger type="submit" value="x">Delete</button></td></tr>' % (str(rule_dict['mailto']),str(rule_dict['action']),str(rule_dict['entity']),str(rule_dict['severity']),str(rule_dict['user']),str(rule_dict['enterprise'])))
                    line_number+=1
                    
        except IOError:
            print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - ERROR: rules.cfg files does not exists or is unreadable"
            return 0
        finally:
                f.close()

        self.wfile.write('''
            <tr>
            <td><input class="span3" type="email" required></td>
            <td><input class="span1" type="text" required></td>
            <td><input class="span2" type="text" required></td>
            <td><input class="span2" type="text" required></td>
            <td><input class="span1" type="text" required></td>
            <td><input class="span1" type="text" required></td>
            <td><button type="button" class="btn btn-info type="submit" value="x">Add</button></td>
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
    def log_message(self, format, *args):
        return
     

    def do_POST(self):
        global rootnode
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                query=cgi.parse_multipart(self.rfile, pdict)
            self.send_response(301)
            
            self.end_headers()
            upfilecontent = query.get('upfile')
            print "filecontent", upfilecontent[0]
            self.wfile.write("<HTML>POST OK.<BR><BR>");
            self.wfile.write(upfilecontent[0]);
        except :
            pass

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


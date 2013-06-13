import string,cgi,time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class ruleEditor(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type',	'text/html')
        self.end_headers()
#        self.wfile.write("hey, today is the" + str(time.localtime()[7]))
#        self.wfile.write(" day in the year " + str(time.localtime()[0]))
        self.wfile.write(''' 
            <html> 
            <head> 
            <title> This is the title </title> 
            </head> 
            <body> 
            <br> 
            <form action="./test.cgi" method="post"> 
            <p> Name: <input type="text" name="name" id="name" value=""/></p> 
            <p> Street Address: <input type="text" name="st_address" id="st_address" value=""/></p> 
            <p> Town: <input type="text" name="town" id="town" value=""/></p> 
            <p> County: <input type="text" name="county" id="county" value=""/></p> 
            <p> Postcode: <input type="text" name="postcode" id="postcode" value=""/></p> 
            <p> Telephone: <input type="text" name="telephone" id="telephone" value=""/></p> 
            <p> Fax: <input type="text" name="fax" id="fax" value=""/></p> 
            <p> Email: <input type="text" name="email" id="email" value=""/></p> 
            <p> Website: <input type="text" name="website" id="website" value=""/></p> 
            <br> 
            <input type="submit" value="Submit" /> 
            </form> 
            </body> 
            </html> 
        ''')

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
            import ConfigParser
            server = HTTPServer(('', rule_editor_port), ruleEditor)
            print 'INFO: Rule editor Webapp started listening at port %s' % (rule_editor_port)
            server.serve_forever()
        except KeyboardInterrupt:
            server.socket.close()


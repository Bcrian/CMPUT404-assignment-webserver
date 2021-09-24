#  coding: utf-8 
import socketserver
import os
import webbrowser

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        request_msg = self.data.decode()
        if request_msg == None:
            self.request.send("HTTP/1.1 400 Bad Request \n".encode())
        else:
            (method, path) = (request_msg.split()[0], request_msg.split()[1])
            if method != 'GET':
                self.request.send("HTTP/1.1 405 Method Not Allowed\n\n".encode('utf-8'))
            else:
                redirected = False
                if os.path.exists("./www" + path + '/index.html'):
                    path += '/index.html'
                    redirected = True
                if path == '/':
                    path = '/index.html'
                elif path.endswith('/'):
                    path += 'index.html'
                
                try:
                    file = open("./www" + path, 'rb')
                    response = file.read()
                    file.close()

                    header = 'HTTP/1.1 200 OK\n'
                    if path.endswith(".html"):
                        mimetype = 'text/html'
                    elif path.endswith(".css"):
                        mimetype = 'text/css'
                    
                    if redirected:
                        header = 'HTTP/1.1 301 Moved Permanently\n' + \
                            'Content-Type: ' + str(mimetype) + '\n\n'
                    else:
                        header += 'Content-Type: ' + str(mimetype) + '\n\n'
                except Exception as e:
                    header = 'HTTP/1.1 404 Not Found\n\n'
                    response = None
                
                final_response = header.encode('utf-8')
                if response:
                    final_response += response
                self.request.send(final_response)
        
        self.request.sendall(bytearray("OK",'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

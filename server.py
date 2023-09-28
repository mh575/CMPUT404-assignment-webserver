#  coding: utf-8 
import socketserver, os

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
        self.data = self.request.recv(1024).strip().decode('utf-8').split('\n')[0].split()[:2] # get method, url 
        print ("Got a request of:\n%s\n" % self.data)
        # self.request.sendall(bytearray("OK\n",'utf-8')) 
        self.handleRequest()
    
    def handleRequest(self):
        self.path = self.data[1]
        if (self.data[0] == "GET"): # GET method only. serve only basehtml, basecss, deephtml, deepcss 
            if (self.data[1][0] == "/"): # url check

                self.path = (os.getcwd()+"\www"+self.data[1]).replace('/','\\') # change front slash to backlash for navigating dir
                print(self.path)
                
                if (os.path.exists(self.path)): # validate path

                    print("path/file exists: "+self.path+"\n")

                    if (self.path[len(self.path)-1] != "\\"): # missing black slash either 301 | file 
                        
                        if (os.path.isfile(self.path)): # .html | .css
                            print("200 file: "+self.path+"\n")
                            self.code200()
                            
                        else: # 301 redirect
                            print("301: "+self.path+"\n")
                            self.code301()

                    else: # url OK
                            self.path += "index.html"
                            print("200 dir: "+self.path)
                            self.code200()

                else: # path/file does not exist
                    print("404 file/path: "+self.path+"\n")
                    self.code404()

            else: # malformed url 
                print("404 url: "+self.path)
                self.code404()

        else: # PUT, POST, PULL methods
            print("405: "+self.path)
            self.code405()

    # format http response 
    def code200(self): 
        code = "200 OK"
        body = open(self.path).read()
        mimeType = self.path.split("\\")[-1].split(".")[1] # get the file ext from the path for mimeType
        self.response = "HTTP/1.1 {}\r\nContent-Type: text/{}; charset=utf-8\r\n\r\n{}".format(code,mimeType,body)
        self.request.sendall(bytearray(self.response, 'utf-8'))
        
    def code301(self): 
        code = "301 Moved Permanently"
        self.path += "index.html"
        location = "http://127.0.0.1:8080"+self.data[1]+"/" # update url from self.data
        self.response = "HTTP/1.1 {}\r\nLocation: {}\r\nContent-Type: text/plain; charset=utf-8\r\n".format(code,location)
        self.request.sendall(bytearray(self.response, 'utf-8'))

    def code404(self):
        code = "404 Not Found"
        self.response = "HTTP/1.1 {}\r\nContent-Type: text/plain; charset=utf-8\r\n".format(code)
        self.request.sendall(bytearray(self.response, 'utf-8'))

    def code405(self):
        code = "405 Method Not Allowed"
        self.response = "HTTP/1.1 {}\r\nContent-Type: text/plain; charset=utf-8\r\n".format(code)
        self.request.sendall(bytearray(self.response, 'utf-8'))
          
        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

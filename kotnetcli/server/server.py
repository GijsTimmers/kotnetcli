#!/usr/bin/python2
import time
import BaseHTTPServer
import CGIHTTPServer
#import ssl

HOST_NAME   = 'localhost'
PORT_NUMBER = 8000
#CERT_FILE   = 'kotnetcli_server.pem'

if __name__ == '__main__':
    handler = CGIHTTPServer.CGIHTTPRequestHandler
    httpd = BaseHTTPServer.HTTPServer((HOST_NAME, PORT_NUMBER), handler)
 #   httpd.socket = ssl.wrap_socket (httpd.socket, certfile=CERT_FILE, server_side=True, ssl_version=ssl.PROTOCOL_TLSv1)

    print time.asctime(), "Kotnetcli Test Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Kotnetcli Test Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
    

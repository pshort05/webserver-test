##!/usr/bin/env python
# -*- coding: utf-8 -*-

from timeme import timeme
import time
import logging
import SocketServer
import ssl
import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SimpleHTTPServer

# -- Defaults --
DEFAULT_PORT = 8000
DEFAULT_SSL_PORT = 4443

# ----> Basic application setup goes here <----
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class GetHandler(BaseHTTPRequestHandler):

    @timeme
    def do_GET(self):
        self.send_response(200)
        self.send_header('Last-Modified', self.date_time_string(time.time()))
        self.end_headers()
        f = open("book.txt")
        self.wfile.write(f.read())
        f.close()
        return


class WebServer(object):

    @classmethod
    def run(cls, port=DEFAULT_PORT, addr='0.0.0.0'):
        httpd = SocketServer.TCPServer((addr, port), GetHandler)
        logging.debug("Running server on port %d", port)
        httpd.serve_forever()


class SSLWebServer:

    @classmethod
    def run(cls, port=DEFAULT_SSL_PORT, addr='0.0.0.0'):
        httpd = HTTPServer((addr, port), SimpleHTTPServer.SimpleHTTPRequestHandler)
        httpd.socket = ssl.wrap_socket(httpd.socket, certfile='./server.pem', server_side=True)
        logging.debug("Running SSL server on port %d", port)
        httpd.serve_forever()

if __name__ == '__main__':
    # Check for the ssl command line option
    if sys.arg[1] == 'ssl':
        SSLWebServer.run()
    else:
        WebServer.run()



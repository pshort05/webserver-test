##!/usr/bin/env python
# -*- coding: utf-8 -*-

from timeme import timeme
import urlparse
import time
import logging
import SimpleHTTPServer
import SocketServer
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler

# -- Program Defaults --
DEFAULT_PORT = 8000

# ---- Basic application setup goes here ----
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class CustomHandler(BaseHTTPServer.BaseHTTPRequestHandler):
   @timeme
    def do_GET(self):
        self.send_response(200)
        self.send_header('Last-Modified', self.date_time_string(time.time()))
        self.end_headers()
        f = open("/Users/paul/git/webserver/index.html")
        self.wfile.write(f.read())
        f.close()
        return


class WebServer(object):
    @classmethod
    def run(cls, port=DEFAULT_PORT):
        #Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        httpd = SocketServer.TCPServer(("", port), CustomHandler)
        logging.debug("Running server on port %d", port)
        httpd.serve_forever()


if __name__ == '__main__':
    WebServer.run()


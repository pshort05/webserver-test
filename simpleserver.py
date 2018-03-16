##!/usr/bin/env python
# -*- coding: utf-8 -*-

# generate server.pem with the following command:
#    openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
# run as follows for the non-ssl version
#    python simpleserver.py
# run as follows for the ssl version#
#    python simpleserver.py ssl
# then in your browser, visit:
#    http://localhost:8080
#    https://localhost:4443

import time
import logging
import SocketServer
import ssl
import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SimpleHTTPServer

# -- Defaults --
DEFAULT_PORT = 8080
DEFAULT_SSL_PORT = 4443

# ----> Basic application setup goes here <----
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print '%r  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000)
        return result
    return timed


class GetHandler(BaseHTTPRequestHandler):

    @timeit
    def do_GET(self):
        logging.debug("Executing do_GET")
        self.send_response(200)
        self.send_header('Last-Modified', self.date_time_string(time.time()))
        self.end_headers()
        f = open("book.txt")
        self.wfile.write(f.read())
        f.close()
        return

class GetSSLHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    @timeit
    def do_GET(self):
        logging.debug("Executing do_GET")
        self.send_response(200)
        self.send_header('Last-Modified', self.date_time_string(time.time()))
        self.end_headers()
        f = open("book.txt")
        self.wfile.write(f.read())
        f.close()
        return

class SSLHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        if self.path == '/get/':
            self.wfile.write('On /get/')
            return
        self.wfile.write('On root')
        return


class WebServer(object):
    @classmethod
    def run(cls, port=DEFAULT_PORT, addr='0.0.0.0'):
        httpd = SocketServer.TCPServer((addr, port), GetHandler)
        logging.debug("Running server on port %d", port)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()


class SSLWebServer(object):
    @classmethod
    def run(cls, port=DEFAULT_SSL_PORT, addr='0.0.0.0'):
        httpd = SocketServer.TCPServer((addr, port), GetHandler)
        httpd.socket = ssl.wrap_socket(httpd.socket, certfile='server.pem', server_side=True)
        logging.debug("Running server on port %d", port)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()


if __name__ == '__main__':
    # Check for the ssl command line option
    logging.debug("%s\n", len(sys.argv))
    if len(sys.argv) > 1:
        logging.debug("%s %s\n", sys.argv[0], sys.argv[1])

        if sys.argv[1] == 'ssl':
            SSLWebServer.run()
    else:
        WebServer.run()





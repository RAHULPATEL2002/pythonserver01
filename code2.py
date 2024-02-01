#!/usr/bin/env python3

import http.server
import socketserver
import os
from urllib.parse import urlparse, parse_qs

class MyHandler(http.server.CGIHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        if parsed_url.path == "/custom-route":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Hello, this is a custom route!</h1></body></html>")
        else:
            # Serve files as usual
            super().do_GET()

# Set the port number
PORT = 8000

# Set the current working directory to the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create the server with the custom handler
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("Server started at port", PORT)
    # Start the server
    httpd.serve_forever()

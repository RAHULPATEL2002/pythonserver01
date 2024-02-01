!/usr/bin/env python3

import http.server
import socketserver

# Set the port number
PORT = 8000

# Create a simple handler to serve files
Handler = http.server.SimpleHTTPRequestHandler

# Create the server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Server started at port", PORT)
    # Start the server
    httpd.serve_forever()

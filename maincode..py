import socket
import os
import mimetypes
import urllib.parse
from datetime import datetime, timedelta

class HTTPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        
    def start(self):
        self.socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}...")
        while True:
            client_socket, client_address = self.socket.accept()
            print(f"Client connected from {client_address}")
            client_handler = HTTPClientHandler(client_socket)
            client_handler.handle_request()

class HTTPClientHandler:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def handle_request(self):
        request_data = self.client_socket.recv(1024).decode()
        method, path, headers, body = self.parse_request(request_data)
        
        if method == "GET":
            self.handle_get(path)
        elif method == "HEAD":
            self.handle_head(path)
        elif method == "POST":
            self.handle_post(path, body)
        elif method == "PUT":
            self.handle_put(path, body)
        elif method == "DELETE":
            self.handle_delete(path)
        else:
            self.send_response(405, "Method Not Allowed", "Allow: GET, HEAD, POST, PUT, DELETE")
        
        self.client_socket.close()

    def parse_request(self, request_data):
        request_lines = request_data.split("\r\n")
        method, path, _ = request_lines[0].split(" ")
        headers = {}
        for line in request_lines[1:]:
            if line:
                key, value = line.split(": ", 1)
                headers[key] = value
        body = request_lines[-1]
        return method, path, headers, body

    def handle_get(self, path):
        if os.path.exists(path):
            with open(path, "rb") as file:
                file_data = file.read()
            content_type, _ = mimetypes.guess_type(path)
            self.send_response(200, "OK", content_type, file_data)
        else:
            self.send_response(404, "Not Found")

    def handle_head(self, path):
        if os.path.exists(path):
            content_type, _ = mimetypes.guess_type(path)
            self.send_response(200, "OK", content_type)
        else:
            self.send_response(404, "Not Found")

    def handle_post(self, path, body):
        # Handle POST requests here
        pass

    def handle_put(self, path, body):
        # Handle PUT requests here
        pass

    def handle_delete(self, path):
        # Handle DELETE requests here
        pass

    def send_response(self, status_code, reason_phrase, content_type=None, body=None):
        response_headers = f"HTTP/1.1 {status_code} {reason_phrase}\r\n"
        if content_type:
            response_headers += f"Content-Type: {content_type}\r\n"
        if body:
            response_headers += f"Content-Length: {len(body)}\r\n"
        response_headers += "\r\n"
        response = response_headers.encode()
        if body:
            response += body
        self.client_socket.sendall(response)

if __name__ == "__main__":
    server = HTTPServer("127.0.0.1", 8080)
    server.start()

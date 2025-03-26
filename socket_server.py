import socket
import os
import time
import threading
import http.server
import socketserver
import json

# Get the port from environment or use default
PORT = int(os.environ.get('PORT', 10000))

# Create a simple HTTP server
class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "status": "success",
            "message": "Socket server is running!",
            "port": PORT,
            "path": self.path
        }
        
        self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        # Override to print to stdout for Render logs
        print(f"Request: {self.path} - {args[0]}")

print(f"Starting socket server on port {PORT}...")
with socketserver.TCPServer(("0.0.0.0", PORT), SimpleHTTPRequestHandler) as httpd:
    print(f"Server started at http://0.0.0.0:{PORT}")
    # This will keep the script running and the port open
    httpd.serve_forever() 
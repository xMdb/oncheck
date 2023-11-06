from dotenv import load_dotenv
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json
import urllib.request

load_dotenv()

api_key = os.getenv("API_KEY")
mc_uuid = os.getenv("MC_UUID")
mc_user = os.getenv("MC_USER")

class RequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, code, message=None):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if message:
            self.wfile.write(bytes(message, "utf8"))

    def do_GET(self):
        # Check the Hypixel API
        with urllib.request.urlopen(f"https://api.hypixel.net/status?uuid={mc_uuid}&key={api_key}") as url:
            data = json.loads(url.read().decode())
            if data["session"]["online"] == False:
                self._send_response(500, f"{mc_user} is offline.")
                return
        self._send_response(200, f"{mc_user} is online.")

def run():
    # Create and run the HTTP server
    port = 8000
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()

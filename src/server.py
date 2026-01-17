#!/usr/bin/env python3
"""
Simple local server for testing the calendar generator API
Run: python server.py
Then open http://localhost:8000/index.html in your browser
"""

import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import sys

# Add api directory to path
sys.path.insert(0, str(Path(__file__).parent / 'api'))

from generate import generate_life_calendar, generate_year_calendar, generate_goal_calendar, LegacyHandler

PORT = 8000

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Handle API requests
        if self.path.startswith('/api/generate'):
            try:
                parsed = urlparse(self.path)
                params = parse_qs(parsed.query)
                
                cal_type = params.get('type', ['goal'])[0]
                w = int(params.get('w', ['1179'])[0])
                h = int(params.get('h', ['2556'])[0])
                w = max(100, min(5000, w))
                h = max(100, min(5000, h))

                if cal_type == 'life':
                    birth = params.get('birth', [''])[0]
                    lifespan = int(params.get('lifes', params.get('lifespan', ['90']))[0])
                    if not birth:
                        raise ValueError("Missing birth parameter")
                    image_bytes = generate_life_calendar(birth, lifespan, w, h)

                elif cal_type == 'year':
                    image_bytes = generate_year_calendar(w, h)

                elif cal_type == 'goal':
                    goal = params.get('goal', ['My Goal'])[0]
                    start = params.get('start', [''])[0]
                    deadline = params.get('deadline', [''])[0]
                    if not start or not deadline:
                        raise ValueError("Missing start or deadline")
                    image_bytes = generate_goal_calendar(goal, start, deadline, w, h)

                else:
                    raise ValueError(f"Unknown type: {cal_type}")

                self.send_response(200)
                self.send_header('Content-Type', 'image/png')
                self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(image_bytes)
                
            except ValueError as e:
                self.send_response(400)
                self.send_header('Content-Type', 'text/plain')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(f'Error: {str(e)}'.encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'text/plain')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(f'Server error: {str(e)}'.encode())
            return
            
        # Serve static files
        return super().do_GET()
    
    def log_message(self, format, *args):
        # Custom log format
        print(f"[{self.log_date_time_string()}] {args[0]}")

if __name__ == "__main__":
    # Change to src directory
    import os
    os.chdir(Path(__file__).parent)
    
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}/")
        print(f"Open http://localhost:{PORT}/index.html in your browser")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")
